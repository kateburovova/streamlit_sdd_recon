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
import crm_processing
import recon

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

df_finance_sdd_loaded = fin_processing.get_df_from_google_spreadsheet(fin_sdd_url, creds, 'daily odessa')
df_finance_sdd = fin_processing.format_fin_data(df_finance_sdd_loaded)
st.dataframe(df_finance_sdd.tail(5))

# loading and processing WH data

# # processing WH data
# df_WH = None
# # if st.button('Process CSV'):
# st.markdown('CSV File Upload and Validation')
# uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
# df_WH = WH_processing.process_csv_upload(uploaded_file)
# if df_WH is not None:
#     _WH_needed = True
#     df_WH, df_WH_sold_sdd, aggregated_WH_by_day = WH_processing.process_WH_data(_WH_needed, df_WH)
#     st.dataframe(df_WH)
# # processing WH data


#############

# processing crm orders
start_date_utc, start_date_utc_normal, end_date_utc = crm_processing.get_timeframe(start_date, end_date)

df_orders_SDD = crm_processing.get_orders_crm(start_date_utc=start_date_utc, end_date_utc=end_date_utc)
payment_types_dict, statuses_dict = crm_processing.get_dicts_crm()

# df_orders_SDD['items_as_string'] = df_orders_SDD['items'].apply(lambda x: str(x))
# df_orders_SDD.drop(columns=['items'], inplace=True)

df_orders_SDD = crm_processing.format_crm_fields(statuses_dict, payment_types_dict, df_orders_SDD)
df_orders_SDD['items_as_string'] = df_orders_SDD['items'].apply(lambda x: str(x))
df_orders_SDD.drop(columns=['items'], inplace=True)

st.write('format_crm_fields done')
st.dataframe(df_orders_SDD)

df_orders_SDD_paid = crm_processing.get_paid_crm_orders(df_orders_SDD, start_date_utc_normal, end_date_utc)

# df_orders_SDD_paid.drop(columns=['items'], inplace=True)
# st.write('get_paid_crm_orders done')
#
# st.dataframe(df_orders_SDD_paid)

total_sum_by_number_fin = recon.get_agg_fin_shipping_data(df_finance_sdd)
st.dataframe(total_sum_by_number_fin)
total_sum_by_number_crm = recon.get_agg_crm_shipping_data(df_orders_SDD_paid)
st.dataframe(total_sum_by_number_crm)

# df_discounts_merged_nonzero = recon.get_discounts_mismatch(df_orders_SDD_paid, df_finance_sdd)
st.write('get_discounts_mismatch done')

# st.write(df_orders_SDD.sample(1).to_dict())
# pc = crm_processing.get_page_count(start_date_utc, end_date_utc)
#
# df_orders_SDD = crm_processing.load_orders(start_date_utc, end_date_utc)
# st.write(len(df_orders_SDD.columns))
# st.write(len(df_orders_SDD))
# st.dataframe(df_orders_SDD)
#
# test_item = df_orders_SDD['items_as_string'].iloc[0]
#
# st.write(test_item)
#
# test_json = crm_processing.string_to_json(test_item)
#
# st.write(test_json[0].keys)
# st.write(test_json)




# df_orders_SDD['items_json'] = df_orders_SDD['items_as_string'].apply(crm_processing.string_to_json)
# st.dataframe(df_orders_SDD)
# df_tst_new = crm_processing.convert_to_original_structure(df_tst)
# # st.dataframe(df_tst_new)
# st.write(df_tst_new.columns)

# df_orders_SDD = crm_processing.get_orders_crm(start_date_utc, end_date_utc)
# st.write(len(df_orders_SDD))
# payment_types_dict, statuses_dict = crm_processing.get_dicts_crm()
# df_orders_SDD = crm_processing.format_crm_fields(statuses_dict, payment_types_dict, df_orders_SDD)
# df_orders_SDD_paid = crm_processing.get_paid_crm_orders(df_orders_SDD, start_date_utc_normal, end_date_utc)
# processing crm orders


# mismatches in discounts

# df_discounts_merged_nonzero = recon.get_discounts_mismatch(df_orders_SDD_paid, df_finance_sdd)
# total_sum_by_number_crm = get_agg_crm_shipping_data(df_orders_SDD_paid)
# test = recon.get_agg_crm_shipping_data(df_orders_SDD_paid)
# st.dataframe(test)

# st.write(df_orders_SDD_paid.iloc[0].to_dict())
# df_orders_SDD = crm_processing.format_crm_fields(statuses_dict, payment_types_dict, df_orders_SDD)
# st.write(len(df_orders_SDD))