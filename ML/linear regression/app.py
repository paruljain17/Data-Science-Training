
from flask import Flask,render_template,request,url_for
import joblib,pickle
import pandas as pd
import sqlite3
#load the model 
model = pickle.load(open('model.pkl','rb'))


app = Flask(__name__)

##database connection

def get_db_connection():
    try:
        conn = sqlite3.connect('bike_db.db')
        #to get the data into dict like format 
        conn.row_factory = sqlite3.Row 
        return conn
    except sqlite3.Error as e:
        print(e)
        return None
    
##create table if not exists
def create_table():
    conn = get_db_connection()
    if conn :
        ##database -->query , fetch , send 
        cursor = conn.cursor()
        cursor.execute("""
                CREATE TABLE IF NOT EXISTS bikes_prediction (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    brand_name TEXT NOT NULL,
                    owner INTEGER NOT NULL,
                    kms_driven INTEGER NOT NULL,
                    age INTEGER NOT NULL,
                    power INTEGER NOT NULL,
                    predicted_price INTEGER NOT NULL
                )
                """)
        conn.commit()
        cursor.close()
        conn.close()
##initialize the database
create_table()

##route history 
@app.route('/history',methods= ['GET',"POST"]) 
def history():
    brand_name_filter = request.form.get('brand_name_filter',None)
    conn = get_db_connection()
    historical_data = []
    if conn : 
        cursor = conn.cursor()
        try:
            if brand_name_filter:
                query = """SELECT * FROM 
                            bikes_prediction WHERE brand_name = ?"""
                cursor.execute(query,(brand_name_filter,))
            else:
                query = """SELECT * FROM bikes_prediction"""
                cursor.execute(query)
            historical_data = cursor.fetchall()

        except sqlite3.Error as e:
            print(e)
        finally:
            cursor.close()
            conn.close()

    return render_template('history.html',historical_data = historical_data)

@app.route('/')
##
def home():
    return render_template('home.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route("/project")
def project():
    return render_template('project.html')

@app.route('/predict',methods=['POST'])
def predict():
    if request.method == "POST":
        try:
            brand_name = request.form['brand_name']
            owner_name = int(request.form['owner'])
            age_bike = int(request.form['age'])
            power_bike = int(request.form['power'])
            kms_driven_bike = int(request.form['kms_driven'])

            bike_numbers = {'TVS': 0,
                                    'Royal Enfield': 1,
                                    'Triumph': 2,
                                    'Yamaha': 3,
                                    'Honda': 4,
                                    'Hero': 5,
                                    'Bajaj': 6,
                                    'Suzuki': 7,
                                    'Benelli': 8,
                                    'KTM': 9,
                                    'Mahindra': 10,
                                    'Kawasaki': 11,
                                    'Ducati': 12,
                                    'Hyosung': 13,
                                    'Harley-Davidson': 14,
                                    'Jawa': 15,
                                    'BMW': 16,
                                    'Indian': 17,
                                    'Rajdoot': 18,
                                    'LML': 19,
                                    'Yezdi': 20,
                                    'MV': 21,
                                    'Ideal': 22}
            
            brand_name_encoded = bike_numbers.get(brand_name)
            input_data = [[owner_name, 
                           brand_name_encoded,
                           kms_driven_bike,
                             age_bike, power_bike]]

            prediction = model.predict(input_data)
            prediction = round(prediction[0],2)


            # ✅ Insert into database
            conn = get_db_connection()
            if conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO bikes_prediction 
                    (brand_name, owner, kms_driven, age, power, predicted_price)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (brand_name, owner_name, kms_driven_bike, age_bike, power_bike, prediction))
                conn.commit()
                cursor.close()
                conn.close()

            return render_template('project.html', prediction=prediction)
            

        except:
            return 'something is wrong'




if __name__ == '__main__':
    app.run(debug=True)
