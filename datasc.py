import streamlit as st
import numpy as np
import pandas as pd
import io
import matplotlib.pyplot as plt

st.set_page_config(page_title="Data Analysis",page_icon="📊",layout="wide")
st.title("📊 Analyze Your Data")
st.write("Upload a **CSV** or an **EXCEL** File To Explore Your Data Interactively")

# Uploading file
upload = st.file_uploader("Upload .csv or .xlxs file", type=["csv","xlsx",'xls'])
if upload is not None:
  try:
    # Get file extension
    extension = upload.name.split(".")[-1].lower()
    if extension == "csv":
      data = pd.read_csv(upload)
      # converting bool columns as str
      bool_cols = data.select_dtypes(include=['bool']).columns
      data[bool_cols] =  data[bool_cols].astype('str')
    elif extension in ["xlsx", "xls"]:
      data = pd.read_excel(upload)
      # converting bool columns as str
      bool_cols = data.select_dtypes(include=['bool']).columns
      data[bool_cols] =  data[bool_cols].astype('str')
    else:
      st.error("Unsupported file format")
      df = None
  except Exception as e:
    st.error("Could Not Read Excel / CSV File. Please Check The File Format")
    st.exception(e)
    st.stop()

  st.success("Upload Successfull!")
  st.write("### Preview of data")
  st.dataframe(data.head())

  st.write("### Data Overview")
  st.write("Number of Rows : ",data.shape[0])
  st.write("Number of Columns : ", data.shape[1])
  # st.write("Number of Missing Values : ",data.isnull().sum())   -->  this syntax will display the result in table manner
  st.write("Number of Missing Values : ",data.isnull().sum().sum())  # this syntax will compute the sum of sum for all columns
  st.write("Number of Duplicate Values : ",data.duplicated().sum())

  st.write("### Complete Summary of Dataset")
  buffer = io.StringIO()
  data.info(buf=buffer)
  i = buffer.getvalue()
  st.text(i)

  st.write("### Statistical Summary of Dataset")
  st.dataframe(data.describe())

  st.write("### Statistical Summary For Non-Numerical Features Of Dataset")
  nonNumCols = data.select_dtypes(include=["bool", "object"])
  if not nonNumCols.empty:
    st.dataframe(data.describe(include=["bool", "object"]))
  else:
    st.info("No non-numerical (object/bool) columns found in the dataset.")

  st.write("### Select The Desired Columns For Analysis")
  selCol = st.multiselect("Choose Columns",data.columns.tolist())

  if selCol:
    st.dataframe(data[selCol].head(20))
  else:
    st.info("No Columns Selected. Showing Full Dataset")
    st.dataframe(data.head())

  st.write("### Data Visualization")
  st.write("Select **Columns** For Data Visualization")
  columns = data.columns.tolist()
  x_axis = st.selectbox("Select Column For X-Axis / Label",options=columns)
  y_axis = st.selectbox("Select Column For Y-Axis / Data",options=columns)

  # Create Buttons For Diff Charts
  col1,col2,col3,col4 = st.columns(4)
  
  with col1:
    lineB = st.button("Click Here To Generate Line Graph")
  with col2:
    scatB = st.button("Click Here To Generate Scatter Graph")
  with col3:
    barB = st.button("Click Here To Generate Bar Graph") 
  with col4:
    pieB = st.button("Click Here to Generate Pie Chart")

  if lineB:
    st.write("### Showing A Line Graph")
    fig,ax = plt.subplots()
    ax.plot(data[x_axis],data[y_axis])
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f"Line Graph Of {x_axis} Vs {y_axis}")
    st.pyplot(fig)

  if scatB:
    st.write("### Showing A Scatter Graph")
    fig,ax = plt.subplots()
    ax.scatter(data[x_axis],data[y_axis])
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f"Scatter Graph Of {x_axis} Vs {y_axis}")
    st.pyplot(fig)

  if barB:
    st.write("### Showing A Bar Graph")
    fig,ax = plt.subplots()
    ax.bar(data[x_axis],data[y_axis])
    ax.set_xlabel(x_axis)
    ax.set_ylabel(y_axis)
    ax.set_title(f"Bar Graph Of {x_axis} Vs {y_axis}")
    st.pyplot(fig)
  
  if pieB:
    st.write("### Showing A Pie Chart")
    fig,ax = plt.subplots()
    ax.pie(
        data[y_axis],
        labels=data[x_axis],
        autopct='%1.1f%%',
        startangle=90
    )
    ax.axis('equal')
    ax.set_title(f"Pie Chart Of {y_axis} and {x_axis}")
    st.pyplot(fig)
  

else:
  st.info("Please Upload A CSV Or An Excel FIle To Get Started")

