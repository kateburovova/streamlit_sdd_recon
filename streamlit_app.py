import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import time
import json
import numpy as np
import pytz

from datetime import datetime, timedelta
st.set_page_config(layout="wide")


st.markdown("## Звіт для звірки даних обліку Slash Dot Dash")

start_date = st.date_input("Оберіть дату початку періоду", datetime.today())
st.write("Обрано:", start_date)

end_date = st.date_input("Оберіть дату кінця періоду", datetime.today())
st.write("Обрано:", end_date)

st.write("crm api url len", len(st.secrets['crm']['cred_api_url']))
st.write("crm api key len", len(st.secrets['crm']['cred_crm_api_key']))
st.write("url fin len", len(st.secrets["google"]["fin_sdd_url"]))

# default
_WH_needed = False



