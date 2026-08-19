import streamlit as st
import pandas as pd
import requests
import http.client
import json

my_ip = requests.get("https://api.ipify.org", timeout=10).text
st.write("Current public IP:", my_ip)

st.set_page_config(page_title="m.Stock option chain", layout="wide")

st.title("Mirae Asset m.Stock option chain")

api_key = str('tl65K+S8+ZX4Q6i1kztrH20cVqafynuY3OLeAuT7Ay0=')

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
#api_key = st.sidebar.text_input("Api key", key='key4', type='password')
submit= st.sidebar.button ("generate otp", key='key3')
if submit== True:
    response = requests.post('https://api.mstock.trade/openapi/typea/connect/login',headers=headers1, data=data1)
    #st.sucess("OTP Sent on registered mobile", key='suc01')

#  ---------------------------------------------------------- Generating OTP--------------------------------------------
OTP = st.sidebar.text_input("Insert OTP to Generate access token", type="password", key='key5')

data2 = {
    'api_key': api_key,
    'request_token': OTP,
    'checksum': 'L',
}

submit1 = st.sidebar.button ("generate session token", key='key6')

if submit1==True:
    response2 = requests.post('https://api.mstock.trade/openapi/typea/session/token', headers=headers1, data=data2)
    st.write(response2)
    response3 = response2.json()
    df1 =st.dataframe(response3)
    st.write(df1)
#  ---------------------------------------------------------- Generating Access Token--------------------------------------------

access_token = st.sidebar.text_input("Acess token", key='key7', type='password')

#exchange = st.sidebar.selectbox("Exchange", options = [1, 4], index = 0, key='key9')
#instrument_token = st.sidebar.text_input("instrument_token", value = 26000, key='key10')
#interval = st.sidebar.selectbox("Interval", options = ['minute', '3minute', '5minute', '10minute', '15minute', '30minute', '60minute', 'day'], index = 2,key='key11')


#  ---------------------------------------------------------- Getting Option Chain details--------------------------------------------
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
    response_text = response5.read().decode("utf-8")
    data = json.loads(response_text)
    st.json(data)

#  ---------------------------------------------------------- Getting NIFTY / Stock Chain details--------------------------------------------

para1 = st.sidebar.selectbox("Choose Exchange", key="key10", options=[1,2,3,4], help="1-NSE, 2-NFO, 3-CDS, 4-BSE, 5-BFO")
para2 = st.sidebar.number_input("Symbol No.", key="key11", value=26000)
st.write(para1)
conn1 = http.client.HTTPSConnection('api.mstock.trade')

conn1.request(
    'GET',
    f'/openapi/typea/instruments/intraday/{para1}/{para2}/5minute',
    headers=headers3
)
response6 = conn1.getresponse()
submit3 = st.sidebar.button("NIFTY /Stock Data", key="key9")

if submit3:
    st.write("HTTP Status:", response6.status)
    st.write(response6)
    response_text2 = response6.read().decode("utf-8")
    data2 = json.loads(response_text2)
    data3 = st.json(data2)


#--------------------------------------------logout--------------------------------------------

logout = st.sidebar.button("Logout", key="key12", type='Primary')

if logout==True:
    requests.post('https://api.mstock.trade/openapi/typea/logout', headers=headers3)






