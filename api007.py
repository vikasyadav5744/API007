
import http.client
import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timezone, date

my_ip = requests.get("https://api.ipify.org", timeout=10).text
st.write("Current public IP:", my_ip)

# ============================================================
                                      # PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="m.Stock NIFTY Option Chain",
    layout="wide"
)

st.title("Mirae Asset m.Stock - NIFTY Option Chain")


#=============================================================
                      #Session State
#============================================================
if "api_key" not in st.session_state:
    st.session_state.api_key=""

if "access_token" not in st.session_state:
    st.session_state.accesstoken=""
    
# ============================================================
                                         # API SETTINGS
# ============================================================

api_key = st.sidebar.text_input(
        "m.Stock Type A API Key",
        type="password", key="api_key")
# ============================================================
                                         # ACCESS TOKEN
# ============================================================
access_token = st.sidebar.text_input("Access Token (optional)",type="password", key="access_token")

#=======================================================================

login_input =st.sidebar.checkbox("show login Inputs", key='key11')

if login_input==True:  
    BASE_URL = "https://api.mstock.trade"
# ============================================================
                                      # LOGIN
# ============================================================
    st.sidebar.header("Login")
    
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input(
        "Password",
        type="password"
    )
    
    if st.sidebar.button("Generate OTP"):
    
        if not username or not password:
            st.error("Enter API Key, Username and Password.")
        else:
    
            login_url = f"{BASE_URL}/openapi/typea/connect/login"
    
            headers = {
                "X-Mirae-Version": "1",
                "Content-Type": "application/x-www-form-urlencoded"
            }
    
            payload = {
                "username": username,
                "password": password
            }
    
            try:
    
                response = requests.post(
                    login_url,
                    headers=headers,
                    data=payload,
                    timeout=15
                )
    
                st.write("Login HTTP Status:", response.status_code)
    
                try:
                    st.json(response.json())
                except:
                    st.write(response.text)
    
                if response.ok:
                    st.success("OTP sent to your registered mobile.")
    
            except Exception as e:
                st.error(f"Login error: {e}")


# ============================================================
                                # GENERATE ACCESS TOKEN
# ============================================================
session_token  =st.sidebar.checkbox("Generate Access Token ", key='key10')

if session_token:
    otp = st.sidebar.text_input(
        "Enter OTP",
        type="password"
    )
    BASE_URL1 = "https://api.mstock.trade"
    if st.sidebar.button("Generate Access Token"):
    
        if not api_key or not otp:
            st.error("Enter API Key and OTP.")
        else:
    
            session_url = f"{BASE_URL1}/openapi/typea/session/token"
    
            headers = {
                "X-Mirae-Version": "1",
                "Content-Type": "application/x-www-form-urlencoded"
            }
    
            payload = {
                "api_key": api_key,
                "request_token": otp,
                "checksum": "L"
            }
    
            try:
    
                response = requests.post(
                    session_url,
                    headers=headers,
                    data=payload,
                    timeout=15
                )
    
                st.write("Session HTTP Status:", response.status_code)
                result = response.json()
                st.json(result)
                #st.session_state.api_key = api_key
           
            except exceptions as e:
                st.write("Error:", e)
            else:
                st.write("nice job")
                st.write("Access token generated successfully")
# ============================================================
# COMMON HEADERS


#  ---------------------------------------------------------- Getting NIFTY / Stock Chain details--------------------------------------------
                      #Intraday Data
#------------------------------------------------------------------------------
conn = http.client.HTTPSConnection('api.mstock.trade')
headers3 = {
          "X-Mirae-Version": "1",
          "Authorization": f"token {api_key}:{access_token}",
      }

Intraday_criteria =st.sidebar.checkbox("show Intraday criteia", key='key20')

if Intraday_criteria==True:
  exchange = st.sidebar.selectbox("Choose Exchange", key="key101", options=[1,2,3,4], help="1-NSE, 2-NFO, 3-CDS, 4-BSE, 5-BFO")
  token = st.sidebar.number_input("Symbol No.", key="key102", value=26000)
  interval = st.sidebar.selectbox("Choose Interval", key="key103", options=['minute','5minute','10minute', '15minute', '30minute', '60minute', 'day'])
  
  #headers3 = {
    #      "X-Mirae-Version": "1",
     #     "Authorization": f"token {api_key}:{access_token}",
     # }
  conn.request(
      'GET',
      f'/openapi/typea/instruments/intraday/{exchange}/{token}/{interval}',
      headers=headers3
  )
  response6 = conn1.getresponse()
  submit3 = st.sidebar.button("NIFTY / Stock Data", key="key109")
  if submit3:
      st.write("HTTP Status:", response6.status)
      response_text2 = response6.read().decode("utf-8")
      data2 = json.loads(response_text2)
      st.json(data2)
    
# ============================================================
# OPTION CHAIN MASTER Expiry data
# ============================================================
chaimaster_criteria =st.sidebar.checkbox("show Expiry criteia", key='key12')
if chaimaster_criteria==True:
    chainmaster =st.sidebar.button("ChainMaster Expiry Data", key='key1')
    if chainmaster:
        try:
            conn.request(
            "GET",
            "/openapi/typea/getoptionchainmaster/2",
            headers=headers3
            )
            response = conn.getresponse()
            st.write("HTTP Status:", response.status)
            st.write("Reason:", response.reason)
            result = response.read().decode("utf-8")
            result = json.loads(result)
            st.json(result)
        except Exception as e:
            st.write("Error:", e)
        finally:
            conn.close()

# ============================================================
# OPTION CHAIN MASTER  CALL / PUT Data
# ============================================================
conn.request(
    'GET',
    f'/openapi/typea/GetOptionChain/2/1795876200/26000',
    headers=headers3)
response101 = conn.getresponse()
st.write("HTTP reason:", response101.reason)
st.write("HTTP status:", response101.status)
result3 = response101.read().decode("utf-8")
data3= json.loads(result3)
st.json(data3)




    


    

