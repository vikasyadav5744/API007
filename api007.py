import streamlit as st
import pandas as pd
import requests
import http.client
import json

my_ip = requests.get("https://api.ipify.org", timeout=10).text
st.write("Current public IP:", my_ip)

st.set_page_config(page_title="m.Stock option chain", layout="wide")

st.title("Mirae Asset m.Stock option chain")

api_key = str('tl65K+S8+ZX4Q6i1kztrH20cVqafynuY3OLeAuT7Ay0=') #type A

#api_key = str('o2yDnj0HapA3uER56rNC+g9rQ3k2nihhUPCRAZtpaK0=') # type B
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
    st.write("OTP Sent on registered mobile")

#  ---------------------------------------------------------- Generating OTP--------------------------------------------

#api_key = st.sidebar.text_input("Api key", key='key4', type='password')
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

#------------------------------------------Script Master ----------------------------------
headers101 = {
    'X-Mirae-Version': '1',
    'Authorization': f"token {api_key}:{access_token}",
}

scriptmaster = st.sidebar.button("Script Master", key="key101")

if scriptmaster==True:
    response101 = requests.get('https://api.mstock.trade/openapi/typea/instruments/scriptmaster', headers=headers101)
    st.write("HTTP Status:", response101.status)
    script =pd.read_csv(response101)
    st.write(script)
    


#  ---------------------------------------------------------- Getting NIFTY / Stock Chain details--------------------------------------------

exchange = st.sidebar.selectbox("Choose Exchange", key="key10", options=[1,2,3,4], help="1-NSE, 2-NFO, 3-CDS, 4-BSE, 5-BFO")
token = st.sidebar.number_input("Symbol No.", key="key11", value=26000)
interval = st.sidebar.selectbox("Choose Interval", key="key16", options=['minute','5minute','10minute', '15minute', '30minute', '60minute', 'day'])
st.write(token)

headers3 = {
        "X-Mirae-Version": "1",
        "Authorization": f"token {api_key}:{access_token}",
    }

conn1 = http.client.HTTPSConnection('api.mstock.trade')

conn1.request(
    'GET',
    f'/openapi/typea/instruments/intraday/{exchange}/{token}/{interval}',
    headers=headers3
)
response6 = conn1.getresponse()

submit3 = st.sidebar.button("NIFTY / Stock Data", key="key9")

if submit3:
    st.write("HTTP Status:", response6.status)
    st.write(response6)
    response_text2 = response6.read().decode("utf-8")
    data2 = json.loads(response_text2)
    data3 = st.json(data2)
    st.write(data3)
#-------------------------------------------------Exchange / Expiry / token ------------------------------

conn4 = http.client.HTTPSConnection('api.mstock.trade')

conn4.request(
    'GET',
    f'openapi/typea/GetOptionChain/{exchange}/1787596200/{token}',
    headers=headers3
)
response7 = conn4.getresponse()

submit4 = st.sidebar.button("exchg / expiry / token", key="key21")

if submit4:
    st.write("HTTP Status:", response7.status)
    st.write(response7)
    response_text3 = response6.read().decode("utf-8")
    data5 = json.loads(response_text3)
    data6 = st.json(data5)
    st.write(data6)

#--------------------------------------------logout--------------------------------------------

logout = st.sidebar.button("Logout", key="key12")

if logout==True:
    requests.post('https://api.mstock.trade/openapi/typea/logout', headers=headers3)
    st.write("logout sucessfully")
