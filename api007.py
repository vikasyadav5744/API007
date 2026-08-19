import streamlit as st
import pandas as pd
import requests
import http.client
import json

my_ip = requests.get("https://api.ipify.org", timeout=10).text
st.write("Current public IP:", my_ip)

st.set_page_config(page_title="m.Stock option chain", layout="wide")

st.title("Mirae Asset m.Stock option chain")

#api_key = str('o2yDnj0HapA3uER56rNC+g9rQ3k2nihhUPCRAZtpaK0=')

# Sidebar
st.sidebar.header("API credentials")
username =st.sidebar.text_input("User Name", key='key1')
password =st.sidebar.text_input("password", type="password", key='key2')

conn = http.client.HTTPSConnection('api.mstock.trade')
headers = {
    'X-Mirae-Version': '1',
    'Content-Type': 'application/json',
}
json_data = {
    'clientcode': username,
    'password': password,
    'totp': '',
    'state': '',
}

submit= st.sidebar.button ("get jwttoken", key='key3')

if submit== True:
    conn.request('POST','/openapi/typeb/connect/login',json.dumps(json_data), headers)
    response = conn.getresponse()
    st.write("HTTP Status:", response.status)
    st.write(response.json())
    


    
