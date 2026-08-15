import streamlit as st
import pandas as pd
from kiteconnect import KiteConnect

st.set_page_config(page_title="Zerodha Option Chain", layout="wide")

st.title("NIFTY option chain - Zerodha Kite Connect")

# Sidebar credentials
st.sidebar.header("Zerodha credentials")
api_key = st.sidebar.text_input("API Key")
access_token = st.sidebar.text_input("Access Token", type="password")

symbol_name = st.selectbox("Select index", ["NIFTY", "BANKNIFTY", "FINNIFTY"])

if st.button("Load option chain"):

    if not api_key or not access_token:
        st.error("Please enter API Key and Access Token")
        st.stop()

    try:
        kite = KiteConnect(api_key=api_key)
        kite.set_access_token(access_token)

        with st.spinner("Downloading instruments..."):
            instruments = pd.DataFrame(kite.instruments("NFO"))

        options = instruments[
            (instruments["name"] == symbol_name) &
            (instruments["segment"] == "NFO-OPT")
        ].copy()

        if options.empty:
            st.error("No option contracts found.")
            st.stop()

        expiries = sorted(options["expiry"].astype(str).unique())
        expiry = st.selectbox("Select expiry", expiries)

        filtered = options[
            options["expiry"].astype(str) == expiry
        ].copy()

        filtered = filtered.sort_values(["strike", "instrument_type"])

        symbols = [f"NFO:{ts}" for ts in filtered["tradingsymbol"]]

        with st.spinner("Fetching live quotes..."):
            quotes = kite.quote(symbols)

        rows = []

        for _, row in filtered.iterrows():
            s = f"NFO:{row.tradingsymbol}"
            q = quotes.get(s, {})

            bid = None
            ask = None

            depth = q.get("depth", {})
            if depth.get("buy"):
                bid = depth["buy"][0].get("price")
            if depth.get("sell"):
                ask = depth["sell"][0].get("price")

            rows.append({
                "Strike": row["strike"],
                "Type": row["instrument_type"],
                "Symbol": row["tradingsymbol"],
                "LTP": q.get("last_price"),
                "OI": q.get("oi"),
                "Volume": q.get("volume"),
                "Bid": bid,
                "Ask": ask
            })

        df = pd.DataFrame(rows)

        st.subheader(f"{symbol_name} option chain ({expiry})")
        st.dataframe(df, use_container_width=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download CSV",
            data=csv,
            file_name=f"{symbol_name}_option_chain_{expiry}.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error: {e}")
