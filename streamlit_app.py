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

start_date = st.date_input("Select a start date", datetime.today())
st.write("You selected:", start_date)
st.write("You selected:", type(start_date))

end_date = st.date_input("Select an enf date", datetime.today())
st.write("You selected:", end_date)

