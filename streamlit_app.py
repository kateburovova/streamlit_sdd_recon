import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import time
import json
import numpy as np
import pytz

from datetime import datetime, timedelta
import fin_processing
import WH_processing

st.set_page_config(layout="wide")


st.markdown("## Звіт для звірки даних обліку Slash Dot Dash")

start_date = st.date_input("Оберіть дату початку періоду", datetime.today())
st.write("Обрано:", start_date)

end_date = st.date_input("Оберіть дату кінця періоду", datetime.today())
st.write("Обрано:", end_date)

# loading creds from secrets
_WH_needed = False
cred_api_url = st.secrets['crm']['cred_api_url']
cred_crm_api_key = st.secrets['crm']['cred_crm_api_key']
fin_sdd_url = st.secrets["google"]["fin_sdd_url"]
creds = {
    'type': st.secrets['google']["type"],
    'project_id': st.secrets['google']["project_id"],
    'private_key_id': st.secrets['google']["private_key_id"],
    'private_key': st.secrets['google']["private_key"],
    'client_email': st.secrets['google']["client_email"],
    'client_id': st.secrets['google']["client_id"],
    'auth_uri': st.secrets['google']["auth_uri"],
    'token_uri': st.secrets['google']["token_uri"],
    'auth_provider_x509_cert_url': st.secrets['google']["auth_provider_x509_cert_url"],
    'client_x509_cert_url': st.secrets['google']["client_x509_cert_url"],
    'universe_domain': st.secrets['google']["universe_domain"]
}

# processing fin data

df_finance_sdd = fin_processing.get_df_from_google_spreadsheet(fin_sdd_url, creds, 'daily odessa')
df_finance_sdd = fin_processing.format_fin_data(df_finance_sdd)
st.dataframe(df_finance_sdd.tail(5))

# loading and processing WH data

# Title of the app
st.markdown('CSV File Upload and Validation')
df_WH = None
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
df_WH = WH_processing.process_csv_upload(uploaded_file)

if df_WH is not None:
    _WH_needed = True
    df_WH, df_WH_sold_sdd, aggregated_WH_by_day = WH_processing.process_WH_data(_WH_needed, df_WH)

st.dataframe(df_WH)


