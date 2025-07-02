#Streamlit
#python library
#webpages for ML and Data Science  projects
#html and css no requirements
import streamlit as st
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import altair as alt
import time
#page configuration
st.set_page_config(
    page_title="streamlit function demo",
    page_icon="😊",
    layout="centered"
)
#title and text elements
st.title("hello world")
st.header("1.Text Elements")
st.subheader("markdown,code,latex")
st.markdown("**bold text**,*italic text*,code text")
st.code("print ('hello )",language="python")
#latex is use for showing the formulaaa
st.latex(r"a^2+b^2=c^2")

st.divider()

#metrices and messages
st.header("2. Metrices and Messages")
st.metric(label="revenue ",value=1234,delta="+10%",delta_color="inverse")
st.error("This is an error message")
st.warning("This is an warning message")
st.info("This is an info message")
st.success("This is an success message")
st.exception(ValueError("this is an exception message"))
st.divider()

#data display
st.header("3.Data Display")
df=pd.DataFrame(np.random.random((10,2)),columns=["a","b"])
st.dataframe(df)
st.table(df.head(3))
st.json(df.to_dict())

st.divider()

#charts
st.header("4. Charts")
st.line_chart(df)
st.bar_chart(df)
st.area_chart(df)
chart= alt.Chart(df.reset_index()).mark_line().encode(x="index",y="a") 
st.altair_chart(chart,use_container_width=True)
fig , ax =plt.subplots()
ax.plot(df.index,df.a)
st.pyplot(fig)
st.divider()

#widgets
st.header("5.Widgets")
with st.form("Input form"):
    name= st.text_input("Enter your name")
    age=st.number_input("Enter your age")
    mood=st.radio("Select your mood",("happy","sad","neutral"))
    languages = st.multiselect("select your languages",("English","French","urdu","german"))
    sumbit = st.form_submit_button("sumbit")
    if sumbit:
        st.success(f"Name:{name},age:{int(age)},mood:{mood},language:{languages}")
st.divider()


col1,col2,col3 = st.columns(3)
with col1:
    name= st.text_input("Enter your name")
    age=st.number_input("Enter your age")
with col2:
    mood=st.radio("Select your mood",("happy","sad","neutral"))
    languages = st.multiselect("select your languages",("English","French","urdu","german"))
with col3:
    st.title("OUTPUT")
    st.title(name)
    st.title(age)
    st.title(mood)
    st.title(languages)
st.divider()

col1,col2=st.columns(2)
with col1:
    number = st.slider("Select a number",0,100)
with col2:
    colour =  st.color_picker("select a color","#37189A")

st.text_area("enter your message")
st.date_input("select a date")
st.time_input("select a time")
st.file_uploader("upload a file")
st.divider()

#media
st.header("6.Media")
st.image("https://th.bing.com/th/id/OIP.2X4KDB--Ll3XHA_qs2XwzQHaE8?w=279&h=187&c=7&r=0&o=7&dpr=1.3&pid=1.7&rm=3")
st.audio("https://open.spotify.com/track/48PA5xbu9RMF48IjZJ5ICs?si=686e99c529f24aab")
#st.video("")


#sidebar
st.sidebar.header("Sidebar header")
st.sidebar.write("this is sdiebar text")
st.sidebar.button("click me")
option = st.sidebar.selectbox("Select an option",("Option 1","Option 2"))


with st.container():
    st.write("this is a container")
with st.expander("expander header"):
    st.write("this is an expander")
with st.spinner("loading Data..."):
     time.sleep(7)
st.toast("toast message",icon="😊")

st.page_link("https://www.geeksforgeeks.org/machine-learning/machine-learning-lifecycle/",label = "gfg", icon="🧐")


















