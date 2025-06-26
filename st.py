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


















