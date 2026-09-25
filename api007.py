import streamlit as st
import pandas as pd
import requests

st.header("Write your code here....")

# Public IP
try:
    my_ip = requests.get(
        "https://api.ipify.org",
        timeout=10
    ).text
    st.write("Current public IP:", my_ip)
except requests.RequestException as e:
    st.error(f"Unable to get public IP: {e}")


# Upload CSV
data = st.file_uploader(
    "Upload CSV file",
    type=["csv"],
    key="upload1"
)

if data is None:

    st.write("Please upload a CSV file.")

else:

    encodings = ["utf-8", "cp1252", "latin1"]

    for encoding in encodings:

        try:
            data.seek(0)

            data1 = pd.read_csv(
                data,
                encoding=encoding
            )

            st.success(f"CSV successfully read using {encoding} encoding.")

            st.dataframe(
                data1,
                use_container_width=True
            )

            break

        except UnicodeDecodeError:
            continue

    else:
        st.error("Could not decode this CSV file using UTF-8, CP1252 or Latin-1.")
