
import http.client
import streamlit as st 
import pandas as pd
import requests
import json
from io import StringIO
from datetime import datetime, timezone, date

my_ip = requests.get("https://api.ipify.org", timeout=10).text
st.write("Current public IP:", my_ip)

data = st.file_uploader("upload file upload", key='upload1', accept_multiple_files=True)
if data is not None:
  data1 = pd.read_excel(data)
  st.write(data1)
else:
  st.write("Upload File Please....")
