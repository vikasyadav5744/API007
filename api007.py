import streamlit as st
import pandas as pd
import requests
import http.client

#      tl65K+S8+ZX4Q6i1kztrH20cVqafynuY3OLeAuT7Ay0= 

st.set_page_config(page_title="m.Stock option chain", layout="wide")

st.title("Mirae Asset m.Stock option chain")

# Sidebar
st.sidebar.header("API credentials")
username =st.sidebar.text_input("User Name", key='key1')
password =st.sidebar.text_input("password", type="password", key='key2')

headers1 = {
    'X-Mirae-Version': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data1 ={
    'username': username,
    'password': password
    }

submit= st.sidebar.button ("generate otp", key='key3')
if submit== True:
    response = requests.post('https://api.mstock.trade/openapi/typea/connect/login',headers=headers1, data=data1)    

api_key = st.sidebar.text_input("Api key", key='key4')
OTP = st.sidebar.text_input("JWT access token", type="password", key='key5')


headers2 = {
    'X-Mirae-Version': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data2 = {
    'api_key': api_key,
    'request_token': OTP,
    'checksum': 'L',
}

submit1 = st.sidebar.button ("generate session token", key='key6')

if submit1==True:
    response2 = requests.post('https://api.mstock.trade/openapi/typea/session/token', headers=headers2, data=data2)
    st.write(response2)
    response3 = response2.json()
    df1 =st.dataframe(response3)
    st.write(df1)


access_token = st.sidebar.text_input("Acess token", key='key7')


conn = http.client.HTTPSConnection('api.mstock.trade')

headers3 = {
    'X-Mirae-Version': '1',
    'Authorization': '{api_key}:{access_token}',
}

conn.request(
    'GET',
    'openapi/typea/instruments/intraday/1/22/minute',
    headers=headers3
)

submit2 = st.sidebar.button ("Get Data", key='key8')

if submit2==True:
    response5 = conn.getresponse()
    st.write(response5)
    df2 =st.dataframe(response5)
    st.write(df2)
    






