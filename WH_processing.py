import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import time
import json
import numpy as np
import pytz

from dicts import status_WH_dict
# @st.cache
def load_file(uploaded_file):
    df = pd.read_csv(uploaded_file)
    return df

def process_WH_data(_WH_needed, df_WH, status_WH_dict = status_WH_dict):
  if _WH_needed:
    cols_to_drop=[' ', 'УУ', 'БУ', 'НУ', 'Валюта', 'Сделка', 'Ответственный', 'Организация', 'Вид операции', 'Вид передачи']
    df_WH = df_WH.drop(columns=[col for col in cols_to_drop if col in df_WH.columns])

    df_WH=df_WH[df_WH['Сумма']!='nan'].copy()
    df_WH['Код CRM'] = df_WH['Код CRM'].astype(str).str.replace('\\xa0', '', regex=False)
    df_WH['Код CRM'] = df_WH['Код CRM'].astype(str).str.replace('\xa0', '', regex=False)

    df_WH['Сумма'] = df_WH['Сумма'].astype(str).str.replace('\u00A0', '', regex=False).str.replace(',', '.').copy()
    df_WH['Сумма'] = df_WH['Сумма'].astype(str).str.replace('\xa0', '', regex=False).str.replace(',', '.').copy()
    df_WH=df_WH[df_WH['Сумма']!='nan'].copy()
    df_WH['Сумма'] = pd.to_numeric(df_WH['Сумма'])
    df_WH['Дата'] = pd.to_datetime(df_WH['Дата'], dayfirst=True)
    df_WH['Date'] = df_WH['Дата'].dt.date

    status_mapping = {value['status_name']: value['status_WH_state'] for key, value in status_WH_dict.items()}
    df_WH['Проведен?'] = df_WH['Статус заказа'].map(status_mapping)

    df_WH_sold_sdd = df_WH[(df_WH['Проведен?']==True)&(df_WH['Подразделение']=='Slash Dot Dash')].copy()

    aggregated_WH_by_day = df_WH_sold_sdd.groupby('Date').agg({
    'Сумма':'sum',
    'Код CRM': lambda x: list(x)}).reset_index()


    aggregated_WH_by_day["Кількість замовлень в обл. тов."] = aggregated_WH_by_day["Код CRM"].apply(lambda x: len(x))

    aggregated_WH_by_day.rename(columns = {'Сумма':'Сумма за обл. тов.',
                                          'Date':'Дата оплати',
                                          'Код CRM':'Список айді CRM (за обл. тов.)'}, inplace=True)

    aggregated_WH_by_day['Дата оплати'] = pd.to_datetime(aggregated_WH_by_day['Дата оплати'])


    aggregated_WH_by_day.sort_values(by='Дата оплати', inplace=True)

    return df_WH, df_WH_sold_sdd, aggregated_WH_by_day

  else:
    return None, None, None


# Function to validate the CSV format

# @st.cache(suppress_st_warning=True)
def process_csv_upload(uploaded_file):
    """
    Process the uploaded CSV file: Read, validate, and display it.

    Parameters:
    uploaded_file: The uploaded file object from Streamlit's file_uploader.
    """
    df = None
    def validate_csv(df):
        """
        Validate the format of the CSV file.

        Parameters:
        df: DataFrame loaded from the CSV file.
        """
        required_columns = ['Код CRM', 'Склад']  # Replace with your actual column names
        return all(column in df.columns for column in required_columns)

    if uploaded_file is not None:
        try:
            df = load_file(uploaded_file)

            if validate_csv(df):
                st.success('CSV format is valid!')
                # # Display the DataFrame in the app (optional)
                # st.dataframe(df)
            else:
                st.error('CSV format is not valid. Please check the required columns.')

        except Exception as e:
            # Catch exceptions that may occur while reading the CSV
            st.error(f'Error reading CSV: {e}')
    return df

