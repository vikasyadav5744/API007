
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

# ============================================================
# API SETTINGS
# ============================================================

api_key = st.sidebar.text_input(
        "m.Stock Type A API Key",
        type="password")
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
            except exceptions as e:
                st.write("Error:", e)
            else:
                st.write("nice job")
                st.write("Access token generated successfully")

# ============================================================
# ACCESS TOKEN
# ============================================================
access_token = st.sidebar.text_input("Access Token (optional)",type="password")
# ============================================================
# COMMON HEADERS
# ============================================================

headers1 = {
    "X-Mirae-Version": "1",
    "Authorization": f"token {api_key}:{access_token}"
}

# ============================================================
# OPTION CHAIN MASTER Expiry data
# ============================================================
chaimaster_criteria =st.sidebar.checkbox("show Expiry criteia", key='key12')
if chaimaster_criteria==True:
    chainmaster =st.sidebar.button("ChainMaster Expiry Data", key='key1')
    if chainmaster:
        try:
            conn = http.client.HTTPSConnection("api.mstock.trade", timeout=10)
            headers4 = {
            "X-Mirae-Version": "1",
            "Authorization": f"token {api_key}:{access_token}"
            }
            conn.request(
            "GET",
            "/openapi/typea/getoptionchainmaster/2",
            headers=headers4
            )
            response = conn.getresponse()
            st.write("HTTP Status:", response.status)
            st.write("Reason:", response.reason)
            result = response.read().decode("utf-8")
            st.write("API Response:")
            st.write(result)
        
        except Exception as e:
            st.write("Error:", e)
        finally:
            conn.close()

# ============================================================
# OPTION CHAIN MASTER  CALL / PUT Data
# ============================================================

call_criteria =st.sidebar.checkbox("show call/ put criteia", key='key13')

if call_criteria==True:
    expiry= st.sidebar.selectbox("Expiry", key='key14', options=[1483021800],index =0)
    exchange1= st.sidebar.selectbox("Exchange", key='key15', options=[1,2],index =1)
    symboltoken1=st.sidebar.number_input("SymbolToken", key='key16', value=26000)
    calldata=st.sidebar.button("Get Call Data", key='key17')
    if calldata:
        try:
            conn = http.client.HTTPSConnection("api.mstock.trade", timeout=10)
            headers5 = {
            "X-Mirae-Version": "1",
            "Authorization": f"token {api_key}:{access_token}"
            }
            conn.request(
            "GET",
            f"/openapi/typea/getoptionchainmaster/{exchange1}/{expiry}/{symboltoken1}",
            headers=headers5
            )
            response1 = conn.getresponse()
            st.write("HTTP Status:", response1.status)
            st.write("Reason:", response1.reason)
            result1 = response1.read().decode("utf-8")
            st.write("API Response:")
            st.write(result1)
        
        except Exception as e:
            st.write("Error:", e)
        finally:
            conn.close()
    


    

