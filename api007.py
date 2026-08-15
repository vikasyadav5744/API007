data
dataX' st
import pandas as pd
import requests

st.set_page_config(page_title="m.Stock option chain", layout="wide")

st.title("Mirae Asset m.Stock option chain")

# Sidebar
st.sidebar.header("API credentials")
username =st.sidebar.text_input("User Name")
password =st.sidebar.text_input("password", type="password")
submit= st.sidebar.button ("generate otp")
api_key = st.sidebar.text_input("API key (X-PrivateKey)")
jwt_token = st.sidebar.text_input("JWT access token", type="password")

headers1 = {
    'X-Mirae-Version': '1',
    'Content-Type': 'application/x-www-form-urlencoded',
}

data1 ={
    'username': username,
    'password': password
    }

if submit== True:
    response = requests.post('https://api.mstock.trade/openapi/typea/connect/login',headers=headers1, data=data1)                     
                        
                             
exchange = st.selectbox(
    "Exchange",
    {
        "NSE FNO": 2,
        "BSE FNO": 4
    }.keys())

expiry = st.text_input("Expiry (YYYY-MM-DD)", "2026-08-27")
underlying_token = st.text_input("Underlying token", "26000")

if st.button("Fetch option chain"):

    if not api_key or not jwt_token:
        st.error("Please enter API key and JWT token.")
        st.stop()

    exch = 2 if exchange == "NSE FNO" else 4

    url = (
        f"https://api.mstock.trade/openapi/typeb/"
        f"getoptionchainmaster/{exch}/{expiry}/{underlying_token}"
    )

    headers = {
        "X-Mirae-Version": "1",
        "Authorization": f"Bearer {jwt_token}",
        "X-PrivateKey": api_key,
        "Content-Type": "application/json"
    }

    try:
        with st.spinner("Fetching option chain..."):
            response = requests.get(url, headers=headers, timeout=15)

        if response.status_code != 200:
            st.error(f"API error {response.status_code}: {response.text}")
            st.stop()

        data = response.json()

        if isinstance(data, dict):
            option_data = (
                data.get("data")
                or data.get("result")
                or data.get("optionChain")
                or []
            )
        else:
            option_data = data

        if not option_data:
            st.warning("No option chain data returned.")
            st.json(data)
            st.stop()

        df = pd.DataFrame(option_data)

        st.success(f"Fetched {len(df)} option contracts")

        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"option_chain_{expiry}.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(str(e))
