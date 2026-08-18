import streamlit as st
import pandas as pd
import requests
import http.client

my_ip = requests.get("https://api.ipify.org", timeout=10).text
st.write("Current public IP:", my_ip)

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
    #st.sucess("OTP Sent on registered mobile", key='suc01')

api_key = st.sidebar.text_input("Api key", key='key4')
OTP = st.sidebar.text_input("Insert OTP to Generate access token", type="password", key='key5')


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

#exchange = st.sidebar.selectbox("Exchange", options = [1, 4], index = 0, key='key9')
#instrument_token = st.sidebar.text_input("instrument_token", value = 26000, key='key10')
#interval = st.sidebar.selectbox("Interval", options = ['minute', '3minute', '5minute', '10minute', '15minute', '30minute', '60minute', 'day'], index = 2,key='key11')

submit2 = st.sidebar.button("Get Data", key="key8")

conn = http.client.HTTPSConnection("api.mstock.trade")
headers3 = {
        "X-Mirae-Version": "1",
        "Authorization": f"token {api_key}:{access_token}",
    }
conn.request(
        "GET",
        "/openapi/typea/getoptionchainmaster/2",
        headers=headers3
    )

response5 = conn.getresponse()

if submit2:
    st.write("HTTP Status:", response5.status)
    st.write(response5)

if response5.status == 200:
    try:
        response6 = json.loads(response_text)
        st.json(response6)
    







