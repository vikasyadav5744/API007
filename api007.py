import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timezone, date

#my_ip= requests.get("https://api.ipify.org", timout=10).text
#st.write("current public IP:", my_ip)



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

def get_option_chain_master():

    url = f"{BASE_URL}/openapi/typea/getoptionchainmaster/2"

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# FIND NIFTY TOKEN AND EXPIRIES
# ============================================================

def get_nifty_information(master):

    data = master.get("data", {})

    # NIFTY underlying token
    nifty_token = None

    for item in data.get("OPTIDX", []):

        parts = item.split(",")

        if len(parts) >= 2:

            symbol = parts[0]
            token = parts[1]

            if symbol.upper() == "NIFTY":
                nifty_token = int(token)
                nifty_expiry_keys = parts[2:]
                break

    if nifty_token is None:
        raise Exception("NIFTY not found in OPTIDX master.")

    # Expiry dictionary
    expiry_dict = data.get("dctExp", {})

    expiries = []

    for expiry_key in nifty_expiry_keys:

        if expiry_key in expiry_dict:

            epoch = int(expiry_dict[expiry_key])

            # Convert epoch to date
            expiry_date = datetime.fromtimestamp(
                epoch,
                tz=timezone.utc
            ).date()

            expiries.append({
                "expiry_key": expiry_key,
                "epoch": epoch,
                "expiry_date": expiry_date
            })

    # Only future/current expiries
    today = date.today()

    expiries = [
        x for x in expiries
        if x["expiry_date"] >= today
    ]

    # Sort nearest expiry first
    expiries.sort(key=lambda x: x["expiry_date"])

    if not expiries:
        raise Exception("No current/future NIFTY expiry found.")

    return nifty_token, expiries


# ============================================================
# GET OPTION CHAIN
# ============================================================

def get_option_chain(expiry_epoch, nifty_token):

    url = (
        f"{BASE_URL}/openapi/typea/"
        f"GetOptionChain/2/{expiry_epoch}/{nifty_token}"
    )

    response = requests.get(
        url,
        headers=headers,
        timeout=15
    )

    response.raise_for_status()

    return response.json()


# ============================================================
# PARSE OPTION CHAIN
# ============================================================

def parse_option_chain(option_data):

    data = option_data.get("data", {})

    call_data = data.get("call", [])
    future_data = data.get("future", [])

    rows = []

    for item in call_data:

        parts = item.split(",")

        if len(parts) >= 3:

            option_token = parts[0]
            strike = parts[1]
            value = parts[2]

            rows.append({
                "Option Token": option_token,
                "Strike": float(strike) / 100,
                "Value": value
            })

    df = pd.DataFrame(rows)

    return df, future_data, data


# ============================================================
# MAIN OPTION CHAIN BUTTON
# ============================================================

st.sidebar.header("NIFTY Option Chain")

if st.sidebar.button("Get Current NIFTY Option Chain"):

    if not api_key:
        st.error("Enter your Type A API Key.")

    elif not access_token:
        st.error("Generate/enter your Access Token.")

    else:

        try:

            # ------------------------------------------------
            # 1. GET MASTER
            # ------------------------------------------------

            with st.spinner("Getting option-chain master..."):

                master = get_option_chain_master()

            # ------------------------------------------------
            # 2. FIND NIFTY + EXPIRY
            # ------------------------------------------------

            nifty_token, expiries = get_nifty_information(master)

            st.success(
                f"NIFTY token: {nifty_token}"
            )

            # ------------------------------------------------
            # 3. DISPLAY EXPIRIES
            # ------------------------------------------------

            expiry_table = pd.DataFrame(expiries)

            expiry_table["expiry_date"] = expiry_table[
                "expiry_date"
            ].astype(str)

            st.subheader("Available NIFTY Expiries")

            st.dataframe(
                expiry_table,
                use_container_width=True
            )

            # ------------------------------------------------
            # 4. CURRENT / NEAREST EXPIRY
            # ------------------------------------------------

            current_expiry = expiries[0]

            expiry_epoch = current_expiry["epoch"]
            expiry_date = current_expiry["expiry_date"]

            st.info(
                f"Current/nearest expiry: "
                f"{expiry_date} | Epoch: {expiry_epoch}"
            )

            # ------------------------------------------------
            # 5. GET OPTION CHAIN
            # ------------------------------------------------

            with st.spinner(
                f"Getting NIFTY option chain for {expiry_date}..."
            ):

                option_data = get_option_chain(
                    expiry_epoch,
                    nifty_token
                )

            # ------------------------------------------------
            # 6. SHOW RAW RESPONSE
            # ------------------------------------------------

            with st.expander("Raw API Response"):

                st.json(option_data)

            # ------------------------------------------------
            # 7. PARSE DATA
            # ------------------------------------------------

            df, future_data, chain_data = parse_option_chain(
                option_data
            )

            # ------------------------------------------------
            # 8. DISPLAY
            # ------------------------------------------------

            st.subheader(
                f"NIFTY Option Chain - {expiry_date}"
            )

            if not df.empty:

                st.dataframe(
                    df,
                    use_container_width=True,
                    height=600
                )

            else:

                st.warning(
                    "No option-chain records were returned."
                )

            # ------------------------------------------------
            # SPOT
            # ------------------------------------------------

            spot = chain_data.get("spot")

            st.write("Spot:", spot)

            # ------------------------------------------------
            # FUTURE
            # ------------------------------------------------

            st.write("Future:", future_data)

        except requests.HTTPError as e:

            st.error(
                f"HTTP error: {e}"
            )

            try:
                st.code(e.response.text)
            except:
                pass

        except Exception as e:

            st.error(
                f"Error: {e}"
            )


# ============================================================
# LOGOUT
# ============================================================

st.sidebar.divider()

if st.sidebar.button("Logout"):

    if access_token:

        logout_url = f"{BASE_URL}/openapi/typea/logout"

        try:

            response = requests.get(
                logout_url,
                headers=headers,
                timeout=15
            )

            st.write(
                "Logout status:",
                response.status_code
            )

            st.session_state.pop(
                "access_token",
                None
            )

            st.success("Logged out.")

        except Exception as e:

            st.error(f"Logout error: {e}")
