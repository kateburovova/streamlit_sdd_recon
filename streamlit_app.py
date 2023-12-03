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

st.set_page_config(layout="wide")


st.markdown("## Звіт для звірки даних обліку Slash Dot Dash")

start_date = st.date_input("Оберіть дату початку періоду", datetime.today())
st.write("Обрано:", start_date)

end_date = st.date_input("Оберіть дату кінця періоду", datetime.today())
st.write("Обрано:", end_date)

# loading creds from secrets
cred_api_url = st.secrets['crm']['cred_api_url']
cred_crm_api_key = st.secrets['crm']['cred_crm_api_key']
fin_sdd_url = st.secrets["google"]["fin_sdd_url"]
creds = {
    'type': st.secrets["type"],
    'project_id': st.secrets["project_id"],
    'private_key_id': st.secrets["private_key_id"],
    'private_key': st.secrets["private_key"],
    'client_email': st.secrets["client_email"],
    'client_id': st.secrets["client_id"],
    'auth_uri': st.secrets["auth_uri"],
    'token_uri': st.secrets["token_uri"],
    'auth_provider_x509_cert_url': st.secrets["auth_provider_x509_cert_url"],
    'client_x509_cert_url': st.secrets["client_x509_cert_url"],
    'universe_domain': st.secrets["universe_domain"]
}

st.write(creds)

# df = fin_processing.get_df_from_google_spreadsheet(fin_sdd_url, creds, 'daily odessa')

# st.write(len(df))

# default
_WH_needed = False



