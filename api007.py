
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

BASE_URL = "https://api.mstock.trade"

# IMPORTANT:
# Do NOT hard-code your real API key in this file.
# Enter it through Streamlit sidebar or secrets.
api_key = st.sidebar.text_input(
    "m.Stock Type A API Key",
    type="password"
)

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

    if not api_key or not username or not password:
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

st.sidebar.header("Session")

otp = st.sidebar.text_input(
    "Enter OTP",
    type="password"
)

if st.sidebar.button("Generate Access Token"):

    if not api_key or not otp:
        st.error("Enter API Key and OTP.")
    else:

        session_url = f"{BASE_URL}/openapi/typea/session/token"

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

            if response.ok:

                # Try common response structures
                access_token = None

                if isinstance(result.get("data"), dict):
                    access_token = (
                        result["data"].get("access_token")
                        or result["data"].get("ACCESS_TOKEN")
                    )

                if access_token:
                    st.session_state["access_token"] = access_token
                    st.success("Access token generated successfully.")

                else:
                    st.warning(
                        "Access token was not found automatically. "
                        "Check the response shown above."
                    )

        except Exception as e:
            st.error(f"Session error: {e}")


# ============================================================
# ACCESS TOKEN
# ============================================================

access_token = st.session_state.get("access_token")

# Optional manual access token
manual_token = st.sidebar.text_input(
    "Access Token (optional)",
    type="password"
)

if manual_token:
    access_token = manual_token
    st.session_state["access_token"] = manual_token


# ============================================================
# COMMON HEADERS
# ============================================================

headers = {
    "X-Mirae-Version": "1",
    "Authorization": f"token {api_key}:{access_token}"
}

# ============================================================
# OPTION CHAIN MASTER
# ============================================================

conn = 'https://api.mstock.trade/openapi/typea/getoptionchainmaster/2'
new=requests.get(conn, headers=headers)
st.write(new)
response = conn.getresponse()
st.write(response.status)
if st.sidebar.button("Chain Master"):
    st.write('HTTPS status:', response.status)
    st.json(response)

    


    

