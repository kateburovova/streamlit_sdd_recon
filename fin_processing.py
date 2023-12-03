import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import requests
import time
import json
import numpy as np
import pytz
from google.oauth2.service_account import Credentials
import gspread

@st.cache
def get_df_from_google_spreadsheet(url, creds, sheet_name):
  """
  Extracts and returns a flattened list of unique values from a DataFrame column that contains lists.

  Parameters:
  - df (pd.DataFrame): The input DataFrame.
  - col (str): The name of the column in the DataFrame that contains lists.
  - col_new_name (str): The name of the new column in which the transformed lists will be stored.

  Returns:
  - list: A flattened list of unique values extracted from the specified DataFrame column.

  Notes:
  - This function assumes that the specified column might contain string representations of lists and handles the transformation.
  - '-1' values are excluded from the final list.

  Example:
  >>> df = pd.DataFrame({'col1': ["[1, 2, 3]", "[2, 3, 4]"]})
  >>> result = get_flat_list_from_col(df, 'col1', 'new_col')
  >>> print(result)
  [1, 2, 3, 4]
  """
  gc = gspread.authorize(Credentials.from_service_account_info(
    creds,
    scopes=['https://spreadsheets.google.com/feeds',
            'https://www.googleapis.com/auth/drive']
  ))
  spreadsheet = gc.open_by_url(url)
  sheet = spreadsheet.worksheet(sheet_name)
  data = sheet.get_all_values()
  df = pd.DataFrame(data)
  df.columns = df.iloc[0]
  df = df.drop(0)
  df.reset_index(inplace=True, drop=True)

  return df
def format_fin_data(df_finance_sdd):

  # drop extra columns and empty rows
  df_finance_sdd.drop(columns = ['порезка', ''], inplace=True)
  columns_to_check = ["Расход или доход", "Какая касса?", "Статья затрат", "Сумма (только цифры с разделителем - точкой)"]
  mask = (df_finance_sdd[columns_to_check] == '').all(axis=1)
  df_finance_sdd = df_finance_sdd[~mask].copy()

  # extract order numbers from the text
  df_finance_sdd['clean_order_number'] = df_finance_sdd['Номер замовлення'].str.extract(r'(\d+)')
  df_finance_sdd['Сумма'] = pd.to_numeric(df_finance_sdd['Сумма (только цифры с разделителем - точкой)'], errors='coerce')

  # clean dates
  df_finance_sdd['datetime'] = pd.to_datetime(df_finance_sdd['дата'], dayfirst=True)
  df_finance_sdd['date'] = df_finance_sdd['datetime'].dt.date

  # cast sums to numeric
  df_finance_sdd['Сумма (только цифры с разделителем - точкой)'] = pd.to_numeric(df_finance_sdd['Сумма (только цифры с разделителем - точкой)'], errors='coerce')
  df_finance_sdd['formatted_sum'] = df_finance_sdd.apply(lambda row: row['Сумма (только цифры с разделителем - точкой)']*(-1) if row['Расход или доход']=='минус' else row['Сумма'], axis=1)

  return df_finance_sdd
