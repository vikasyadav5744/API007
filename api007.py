import streamlit as st
import pandas as pd
import requests

st.header("Write your code here....")

# Get public IP
try:
    my_ip = requests.get("https://api.ipify.org", timeout=10).text
    st.write("Current public IP:", my_ip)
except requests.RequestException as e:
    st.error(f"Unable to get public IP: {e}")

# File uploader
data = st.file_uploader(
    "Upload Excel file",
    type=["xlsx", "xls"],
    key="upload1"
)

if data is None:
    st.write("Please upload an Excel file.")
else:
    try:
        data1 = pd.read_excel(data)
        st.write("Uploaded data:")
        st.dataframe(data1, use_container_width=True)
    except Exception as e:
        st.error(f"Error reading Excel file: {e}")
