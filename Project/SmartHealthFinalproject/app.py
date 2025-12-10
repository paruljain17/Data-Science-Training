from flask import Flask, render_template, request
import numpy as np
import pickle
import os
from tensorflow.keras.models import load_model

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

# ---- PATHS: update if necessary ----
MODEL_PATH = "heart_model.h5"
SCALER_PATH = "scaler.pkl"

# ---- Load model & scaler ----
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"Model not found: {MODEL_PATH}")
model = load_model(MODEL_PATH)

if not os.path.exists(SCALER_PATH):
    raise FileNotFoundError(f"Scaler not found: {SCALER_PATH}")
with open(SCALER_PATH, "rb") as f:
    scaler = pickle.load(f)

# ---- Feature order expected by model ----
FEATURE_ORDER = ["age","sex","cp","trestbps","chol","fbs",
                 "restecg","thalach","exang","oldpeak","slope","ca","thal"]

# ---- Medians / defaults computed from training (adjust if you have exact medians) ----
MEDIANS = {
    "trestbps": 130,
    "chol": 200,
    "restecg": 0,
    "thalach": 150,
    "oldpeak": 1.0,
    "slope": 1,
    "ca": 0,
    "thal": 1
}

# ---- Mapping from easy-questions to advanced params ----
def map_easy_to_advanced(form):
    """
    form: request.form (ImmutableMultiDict)
    returns dict of mapped/filled values for advanced fields
    """
    mapped = {}
    # If user provided explicit advanced inputs (from advanced section), use them
    for key in ["restecg","thalach","oldpeak","slope","ca","thal"]:
        val = form.get(key)
        if val and val.strip() != "" and val != "dontknow":
            try:
                mapped[key] = float(val) if "." in val else int(val)
            except:
                mapped[key] = MEDIANS.get(key)
        else:
            mapped[key] = None

    # Map easy questions if advanced fields not provided
    # Example: exercise pain -> exang
    exag = form.get("exang_easy")  # "yes"/"no"/"dontknow"
    if mapped.get("exang") is None:
        # we'll set exang from user toggle if present
        pass

    # fill exang (exercise angina) from toggle (yes->1,no->0)
    exang_toggle = form.get("exang_toggle")
    if exang_toggle in ("yes","no"):
        mapped["exang"] = 1 if exang_toggle=="yes" else 0
    else:
        mapped["exang"] = 0  # default

    # oldpeak mapping: simple Q about symptoms
    symp = form.get("symptom_after_exercise")  # yes/no/dontknow
    if mapped["oldpeak"] is None:
        if symp == "yes":
            mapped["oldpeak"] = 1.5
        elif symp == "no":
            mapped["oldpeak"] = 0.2
        else:
            mapped["oldpeak"] = MEDIANS["oldpeak"]

    # slope mapping: ask "Any problem reported in stress test?"
    stress = form.get("stress_test_problem")  # yes/no/dontknow
    if mapped["slope"] is None:
        if stress == "yes":
            mapped["slope"] = 2
        elif stress == "no":
            mapped["slope"] = 0
        else:
            mapped["slope"] = MEDIANS["slope"]

    # restecg: if user says "abnormal ECG" or not
    ecg_q = form.get("ecg_easy")  # normal/abnormal/dontknow
    if mapped["restecg"] is None:
        if ecg_q == "normal":
            mapped["restecg"] = 0
        elif ecg_q == "abnormal":
            mapped["restecg"] = 1
        else:
            mapped["restecg"] = MEDIANS["restecg"]

    # thal & ca: angiography/thallium question
    angi = form.get("angiography")  # none/yes_known/unknown
    if mapped["ca"] is None:
        if angi == "none":
            mapped["ca"] = 0
        elif angi == "yes_known":
            # if user says yes but doesn't know number, assume 1
            mapped["ca"] = 1
        else:
            mapped["ca"] = MEDIANS["ca"]

    thal_q = form.get("thal_easy")  # normal/fixed/reversible/dontknow
    if mapped["thal"] is None:
        if thal_q == "normal":
            mapped["thal"] = 0
        elif thal_q == "fixed":
            mapped["thal"] = 1
        elif thal_q == "reversible":
            mapped["thal"] = 2
        else:
            mapped["thal"] = MEDIANS["thal"]

    # thalach: if user knows max HR else median
    if mapped["thalach"] is None:
        t = form.get("thalach")
        if t and t.strip() != "" and t != "dontknow":
            try:
                mapped["thalach"] = int(t)
            except:
                mapped["thalach"] = MEDIANS["thalach"]
        else:
            mapped["thalach"] = MEDIANS["thalach"]

    # ensure types are correct
    for k in mapped:
        if mapped[k] is None:
            mapped[k] = MEDIANS.get(k, 0)

    return mapped

def prepare_feature_vector(form):
    x = []
    # basic fields with safe defaults
    for f in ["age","sex","cp","trestbps","chol","fbs"]:
        val = form.get(f)
        if val is None or val.strip()=="" or val=="dontknow":
            # fill medians or sensible default
            if f in ["trestbps","chol"]:
                val = MEDIANS.get(f)
            elif f=="fbs":
                val = 0
            else:
                val = 0
        # cast
        try:
            if "." in str(val):
                val = float(val)
            else:
                val = int(val)
        except:
            val = float(val) if str(val).count(".") else int(val)
        x.append(val)

    # advanced mapping
    adv = map_easy_to_advanced(form)
    # order: restecg, thalach, exang, oldpeak, slope, ca, thal
    x.append(int(adv.get("restecg", MEDIANS["restecg"])))
    x.append(int(adv.get("thalach", MEDIANS["thalach"])))
    x.append(int(adv.get("exang", 0)))
    x.append(float(adv.get("oldpeak", MEDIANS["oldpeak"])))
    x.append(int(adv.get("slope", MEDIANS["slope"])))
    x.append(int(adv.get("ca", MEDIANS["ca"])))
    x.append(int(adv.get("thal", MEDIANS["thal"])))

    arr = np.array(x).reshape(1, -1)
    return arr

@app.route("/", methods=["GET","POST"])
def index():
    result = None
    if request.method == "POST":
        # 1. Prepare feature vector
        x = prepare_feature_vector(request.form)
        # 2. Scale
        try:
            x_scaled = scaler.transform(x)
        except Exception as e:
            # fallback: if scaler can't transform, use as-is
            print("Scaler transform error:", e)
            x_scaled = x

        # 3. Get probability (Keras model with sigmoid output)
        try:
            pred_raw = model.predict(x_scaled).ravel()
            # If shape (1,) treat as probability; if model outputs logits, apply sigmoid?
            prob = float(pred_raw[0]) if hasattr(pred_raw, "__len__") else float(pred_raw)
            # In some models predict gives value >1 (rare), clamp:
            prob = max(0.0, min(1.0, prob))
        except Exception:
            # try sklearn style
            try:
                prob = float(model.predict_proba(x_scaled)[:,1])
            except Exception as e:
                print("Prediction error:", e)
                prob = 0.0

        # 4. Threshold (tunable)
        THRESH = 0.35  # you can tune based on validation; lower -> more sensitive
        pred_label = int(prob >= THRESH)

        result = {
            "probability": round(prob, 3),
            "pred": pred_label,
            "message": "Higher risk — Please consult a physician." if pred_label==1 else "Lower risk — If symptoms exist, consult doctor.",
            "threshold": THRESH
        }

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
