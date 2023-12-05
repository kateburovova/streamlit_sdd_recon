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


st.markdown("# Звіт для звірки даних обліку SDD")

st.markdown("### Як працює цей звіт?")

st.markdown('Цей звіт автоматично отримує актуальні дані з Finance та CRM при кожному провантаженні. '
            'Дані з системи обліку товарів можна завантажити опціонально. '
            'Якщо ви підвантажите файл з даними з системи обліку товарів, до звіта додасться таблиця з порівнянням суми і статуса замовлення в CRM та системі обліку товарів. '
            'Також до порівняння денних кас буде додано колонки з даними з системи обліку товарів. '
            'Звіт обробляється покроково, тобто спочатку вам потрібно обрати потрібні дати, а потім - чи завантажувати файл обліку товарів. ')

start_date = st.date_input("Оберіть дату початку періоду", datetime.today())
st.write("Обрано:", start_date)

end_date = st.date_input("Оберіть дату кінця періоду", datetime.today())
st.write("Обрано:", end_date)

st.markdown('Дані з CRM отримуються за датою створення замовлення, а не за датою оплати. '
            'Тож для того, щоб не пропустити старі замовлення оплачені в поточному періоді, до дати початку додається 1 місяць (наприклад, обравши 1 листопада до 30 листопада, система завантажить дані з 1 жовтня.) '
            'Це означає, що дуже старі замовлення (старші за місяць до початку періода) не будуть включені в звіт, навіть якщо вони оплачені зараз. '
            'За замовчанням дати звіту встановлюються з сьогодні по сьогодні, тож якщо вам потрібні інші дати, не чекайте, поки дані завантажаться за замовчанням і відразу обирайте правильний період. '
            'Завантаження всіх даних і їх обробка триватиме в середньому 5-7 хвилин (прям пропорційно залежить від довжини обраного періоду). ')

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
# st.dataframe(df_finance_sdd.tail(5))

# loading and processing WH data

# processing WH data

WH_options = ['Так', 'Ні']
selected_WH_option = st.radio('Оберіть, будь ласка, чи завантажувати файл з обліку товарів :', WH_options, key='wh_option')
df_WH = None
aggregated_WH_by_day = None
df_WH_sold_sdd = None


if selected_WH_option=='Так':
    st.markdown('Завантажте CSV File з документами реалізації за обраний період.')
    uploaded_file = st.file_uploader("Оберіть CSV файл", type="csv")
    df_WH = WH_processing.process_csv_upload(uploaded_file)
    if df_WH is not None:
        _WH_needed = True
        df_WH, df_WH_sold_sdd, aggregated_WH_by_day = WH_processing.process_WH_data(_WH_needed, df_WH)
else:
    st.write("Не завантажуємо файл 👌")

# st.write('Починається завантаження і обробка даних, зачекайте ⏳')

#############

# processing crm orders
start_date_utc, start_date_utc_normal, end_date_utc = crm_processing.get_timeframe(start_date, end_date)

df_orders_SDD = crm_processing.get_orders_crm(start_date_utc=start_date_utc, end_date_utc=end_date_utc)
payment_types_dict, statuses_dict = crm_processing.get_dicts_crm()

df_orders_SDD = crm_processing.format_crm_fields(statuses_dict, payment_types_dict, df_orders_SDD)
df_orders_SDD['items_as_string'] = df_orders_SDD['items'].apply(lambda x: str(x))
df_orders_SDD.drop(columns=['items'], inplace=True)

# st.dataframe(df_orders_SDD)
df_orders_SDD_paid = crm_processing.get_paid_crm_orders(df_orders_SDD, start_date_utc_normal, end_date_utc)


st.write('************************************')
st.markdown('### Порівняння знижок за даними CRM та даними Finance')
st.markdown('Дані виводяться з обраний період.')
df_discounts_merged_nonzero = recon.get_discounts_mismatch(df_orders_SDD_paid, df_finance_sdd)
df_discounts_merged_nonzero.rename(columns={'clean_order_number':'Номер замовлення',
                                           'discountTotal':'Знижка в CRM',
                                           'Сумма':'Знижка в Finance',
                                           'diff':'Розбіжність'}, inplace=True)
st.dataframe(df_discounts_merged_nonzero)

st.write('************************************')
st.markdown('### Порівняння сум, оплачених нам за доставку за даними CRM та даними Finance')
st.markdown('Дані виводяться з обраний період. Якщо ви не вказали номер замовлення в рядку Finance, сума знижки не потрапить в цей звіт. ')
df_delivery_payed_mismatch = recon.get_delivery_payed_mismatch(df_finance_sdd, df_orders_SDD_paid)
df_delivery_payed_mismatch.rename(columns={'clean_order_number':'Номер замовлення',
                                           'discountTotal':'Знижка в CRM',
                                           'Сумма':'Знижка в Finance',
                                           'diff':'Розбіжність'}, inplace=True)
st.dataframe(df_delivery_payed_mismatch)


st.write('************************************')
st.markdown('### Порівняння сум та замовлень за день за даними CRM, Finance та обліку товарів (коли підвантажений)')
st.markdown('Дані виводяться з обраний період. Якщо ви бачите порожній бабл на місці номера замовлення, значить, якесь замовлення є, але без вказання номера. ')
filtered_df = recon.get_timed_daily_data(df_finance_sdd, df_orders_SDD_paid, start_date_utc_normal, end_date_utc)
filtered_df = recon.format_daily_timed_data(filtered_df)
final_df = recon.get_final_daily_comparison(filtered_df, _WH_needed, aggregated_WH_by_day)
st.dataframe(final_df)


st.write('************************************')
st.markdown('### Порівняння статусів і сум замовлень за даними CRM та системи обліку товарів')
df_by_number_final = recon.compare_crm_and_WH_data(df_orders_SDD_paid, df_WH_sold_sdd, _WH_needed)

if _WH_needed:
    st.markdown('Дані виводяться з обраний період. '
                'Код CRM - це не назва замовлення, а айді з посилання (в системі обліку товару також присутнє це поле). ')
    df_by_number_final.rename(columns={'Проведен?':'Проведено в CRM',
                                       'status_WH':'Проведено в базі',
                                       'Сумма':'Сума в базі',
                                       'totalSumm':'Сума в CRM',
                                       'clean_order_number':'Номер замовлення в CRM',
                                       'Номер':'Номер документу реалізації в базі',
                                       'status_name':'Статус в CRM',
                                       'Статус':'Статус в базі'}, inplace=True)

    st.dataframe(df_by_number_final)

