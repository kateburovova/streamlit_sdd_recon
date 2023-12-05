import pandas as pd
import streamlit as st
import requests
import time
import json
import numpy as np
import pytz
from google.oauth2.service_account import Credentials
import gspread

from dicts import new_order_with_WH
from dicts import new_order_no_WH
from dicts import cols_to_show_status_comparison


def filter_and_aggregate_by_payment_by_date(df, payment_field_name, date_field_name, sum_field_name, order_field_name):
    df_filtered=df[~df[date_field_name].isna()].copy()
    payment_types = list(df_filtered[payment_field_name].value_counts().index)
    filtered_dfs = {}
    aggregated_filtered = {}

    for kassa in payment_types:
        if kassa!='':
            df_iter = df_filtered[df_filtered[payment_field_name]==kassa].copy()
            filtered_dfs[kassa] = df_iter
            total_sum_name = f'Загалом по {kassa} в CRM'
            order_list_name = f'Список замовлень по {kassa} в CRM'
            order_count_name = f'Кількість замовлень по {kassa} в CRM'
            aggregated_filtered_df = df_iter.groupby(date_field_name).agg({
                sum_field_name: 'sum',
                order_field_name: lambda x: list(x)}).reset_index()
            aggregated_filtered_df[order_count_name] = aggregated_filtered_df[order_field_name].apply(lambda x: len(x))
            aggregated_filtered_df = aggregated_filtered_df.sort_values(by=date_field_name)
            aggregated_filtered_df.rename(columns={order_field_name:order_list_name,
                                                   sum_field_name: total_sum_name,
                                                   'payment_date': 'Дата оплати'}, inplace=True)
            aggregated_filtered[kassa] = aggregated_filtered_df

    return aggregated_filtered

def get_agg_fin_shipping_data(df_finance_sdd):
    df_finance_sdd_discount = df_finance_sdd[df_finance_sdd['Статья затрат'].str.contains('скидка', na=False)]
    total_sum_by_number_fin = df_finance_sdd_discount.groupby('clean_order_number')['Сумма'].sum().reset_index()

    return total_sum_by_number_fin

def get_agg_crm_shipping_data(df_orders_SDD_paid):
    total_sum_by_number_crm = df_orders_SDD_paid.groupby('clean_order_number')['discountTotal'].sum().reset_index()

    return total_sum_by_number_crm

def get_discounts_mismatch(df_orders_SDD_paid, df_finance_sdd):
    total_sum_by_number_fin = get_agg_fin_shipping_data(df_finance_sdd)
    total_sum_by_number_crm = get_agg_crm_shipping_data(df_orders_SDD_paid)
    df_discounts_merged = total_sum_by_number_crm.merge(total_sum_by_number_fin,how='left', on='clean_order_number')
    df_discounts_merged['diff'] = np.where(
        df_discounts_merged['Сумма'].isna(),
        np.nan,
        df_discounts_merged['discountTotal'] - df_discounts_merged['Сумма'])
    df_discounts_merged_clean=df_discounts_merged[~df_discounts_merged['diff'].isna()].copy()
    df_discounts_merged_nonzero = df_discounts_merged_clean[df_discounts_merged_clean['diff']!=0]

    return df_discounts_merged_nonzero

def get_agg_crm_shipping_advances(df_orders_SDD_paid):
    df_NP_paid_to_us_crm = df_orders_SDD_paid[df_orders_SDD_paid['delivery_cost_paid_to_us'] != 0].copy()
    aggregated_df = df_NP_paid_to_us_crm.groupby('payment_date').agg({
        'delivery_cost_paid_to_us': 'sum',
        'clean_order_number': 'count',
        'clean_order_number': lambda x: list(x)
    }).reset_index()

    # Rename the column for clarity
    aggregated_df = aggregated_df.rename(columns={'payment_date': 'Дата',
                                                  'clean_order_number': 'Номери за crm',
                                                  'delivery_cost_paid_to_us': 'Cумарно отримано оплат доставки за crm'})
    return aggregated_df

def get_agg_fin_shipping_advances(df_finance_sdd):
    filtered_df_fin_NP = df_finance_sdd[
        (df_finance_sdd['Расход или доход'] == 'минус') &
        (df_finance_sdd['Сумма (только цифры с разделителем - точкой)'] < 0) &
        (df_finance_sdd['Статья затрат'] == 'перевозки: НП отправки покупателям за наш счет')
        ]
    filtered_df_fin_NP

    aggregated_df_fin = filtered_df_fin_NP.groupby('date').agg({
        'Сумма (только цифры с разделителем - точкой)': 'sum',
        'clean_order_number': 'count',
        'clean_order_number': lambda x: list(x)
    }).reset_index()

    aggregated_df_fin = aggregated_df_fin.rename(columns={'date': 'Дата',
                                                'clean_order_number': 'Номери за Finance',
                                                'Сумма (только цифры с разделителем - точкой)': 'Cумарно отримано оплат доставки за Finance'})

    return aggregated_df_fin

def get_delivery_payed_mismatch(df_finance_sdd, df_orders_SDD_paid):
    aggregated_df_fin = get_agg_fin_shipping_advances(df_finance_sdd)
    aggregated_df = get_agg_crm_shipping_advances(df_orders_SDD_paid)

    df_delivery_payed_mismatch = aggregated_df.merge(aggregated_df_fin, how='outer', on='Дата')
    df_delivery_payed_mismatch['Cумарно отримано оплат доставки за crm'] = df_delivery_payed_mismatch['Cумарно отримано оплат доставки за crm'].fillna(0.0)
    df_delivery_payed_mismatch['Cумарно отримано оплат доставки за Finance'] = df_delivery_payed_mismatch['Cумарно отримано оплат доставки за Finance'].fillna(0.0)
    df_delivery_payed_mismatch['Номери за crm'] = df_delivery_payed_mismatch['Номери за crm'].apply(lambda x: x if isinstance(x, list) else [])
    df_delivery_payed_mismatch['Номери за Finance'] = df_delivery_payed_mismatch['Номери за Finance'].apply(lambda x: x if isinstance(x, list) else [])

    df_delivery_payed_mismatch['Розбіжність (crm мінус Finance)'] = df_delivery_payed_mismatch['Cумарно отримано оплат доставки за crm']+df_delivery_payed_mismatch['Cумарно отримано оплат доставки за Finance']

    df_delivery_payed_mismatch['Розбіжність по номерах (є в crm, немає в Finance)'] = \
        df_delivery_payed_mismatch.apply(lambda row:
                                     list(set(row['Номери за crm']) - set(row['Номери за Finance'])),
                                     axis=1)

    df_delivery_payed_mismatch['Розбіжність по номерах (є в Finance, немає в crm)'] = \
        df_delivery_payed_mismatch.apply(lambda row:
                                      list(set(row['Номери за Finance'])-set(row['Номери за crm'])),
                                      axis=1)
    df_delivery_payed_mismatch.sort_values(by='Дата', inplace=True)

    return df_delivery_payed_mismatch

def get_daily_agg_fin_dfs(df_finance_sdd):
    filtered_dfs = {}

    aggregated_filtered_dfs = {}

    for kassa in list(df_finance_sdd['Какая касса?'].value_counts().index):
        if kassa!='':
            df = df_finance_sdd[(df_finance_sdd['Какая касса?']==kassa)\
                          &((df_finance_sdd['Статья затрат']=='')\
                            |(df_finance_sdd['Статья затрат']=='скидка')\
                            |(df_finance_sdd['Статья затрат']=='перевозки: НП отправки покупателям за наш счет'))].copy()
            filtered_dfs[kassa] = df

            total_sum_name = f'Загалом по {kassa} в Fin'
            order_list_name = f'Список замовлень по {kassa} в Fin'
            order_count_name = f'Кількість замовлень по {kassa} в Fin'

            aggregated_filtered_df = df.groupby('date').agg({
                'formatted_sum': 'sum',
                'clean_order_number': lambda x: list(x)}).reset_index()


            aggregated_filtered_df = aggregated_filtered_df.sort_values(by='date')

            aggregated_filtered_df.rename(columns={'clean_order_number':order_list_name,
                                            'formatted_sum': total_sum_name,
                                            'date': 'Дата оплати'}, inplace=True)
            aggregated_filtered_df[order_list_name] = aggregated_filtered_df[order_list_name].apply(lambda x: list(set(x)))
            aggregated_filtered_df[order_count_name] = aggregated_filtered_df[order_list_name].apply(lambda x: len(x))

            aggregated_filtered_dfs[kassa] = aggregated_filtered_df

    return aggregated_filtered_dfs


def merge_dataframes_on_date(dict1, dict2):
    """
    Merges all DataFrames from two dictionaries into a single DataFrame on the 'Дата' column using an outer merge.

    Parameters:
    - dict1 (dict): The first dictionary of DataFrames.
    - dict2 (dict): The second dictionary of DataFrames.

    Returns:
    pd.DataFrame: A merged DataFrame containing all DataFrames from both dictionaries.
    """
    # Initialize the merged DataFrame with the first DataFrame from either dictionary
    all_dfs = list(dict1.values()) + list(dict2.values())

    if not all_dfs:
        return pd.DataFrame()  # Return an empty DataFrame if there are no DataFrames to merge

    merged_df = all_dfs[0].copy()

    # Merge each subsequent DataFrame
    for df in all_dfs[1:]:
        merged_df = pd.merge(merged_df, df, on='Дата оплати', how='outer', suffixes=('', '_dup'))

    # Drop duplicate columns if any
    for col in merged_df.columns:
        if '_dup' in col:
            merged_df.drop(col, axis=1, inplace=True)

    return merged_df

def get_timed_daily_data(df_finance_sdd, df_orders_SDD_paid, crm_start_date, crm_end_date):
    aggregated_crm_dfs = filter_and_aggregate_by_payment_by_date(df = df_orders_SDD_paid,
                                                               payment_field_name ='payment_type_name',
                                                               date_field_name ='payment_date',
                                                               sum_field_name='totalSumm',
                                                               order_field_name ='clean_order_number')

    aggregated_filtered_dfs = get_daily_agg_fin_dfs(df_finance_sdd)
    merged_df = merge_dataframes_on_date(aggregated_crm_dfs, aggregated_filtered_dfs)
    merged_df['Дата оплати'] = pd.to_datetime(merged_df['Дата оплати'])
    _start_date = pd.Timestamp(crm_start_date)
    _end_date = pd.Timestamp(crm_end_date)
    filtered_df = merged_df[(merged_df['Дата оплати'] >= crm_start_date) & (merged_df['Дата оплати'] <= crm_end_date)].copy()
    filtered_df.sort_values(by='Дата оплати', inplace=True)

    return filtered_df

def get_col_lists(filtered_df):
    crm_total_columns = [col for col in filtered_df.columns if 'CRM' in col and 'Загалом' in col]
    fin_total_columns = [col for col in filtered_df.columns if 'Fin' in col and 'Загалом' in col]

    crm_qtty_columns = [col for col in filtered_df.columns if 'CRM' in col and 'Кількість' in col]
    fin_qtty_columns = [col for col in filtered_df.columns if 'Fin' in col and 'Кількість' in col]

    crm_list_columns = [col for col in filtered_df.columns if 'CRM' in col and 'Список' in col]
    fin_list_columns = [col for col in filtered_df.columns if 'Fin' in col and 'Список' in col]

    return crm_total_columns, fin_total_columns, crm_qtty_columns, fin_qtty_columns, crm_list_columns, fin_list_columns

def replace_nan_with_empty_list(x):
    if isinstance(x, list):
        return x
    if pd.isna(x):
        return []
    return x

def format_daily_timed_data(filtered_df):
    crm_total_columns, fin_total_columns, crm_qtty_columns, fin_qtty_columns, crm_list_columns, fin_list_columns = get_col_lists(filtered_df)

    for col in fin_list_columns:
        filtered_df[col] = filtered_df[col].apply(replace_nan_with_empty_list)

    for col in crm_list_columns:
        filtered_df[col] = filtered_df[col].apply(replace_nan_with_empty_list)


    filtered_df[crm_total_columns] = filtered_df[crm_total_columns].fillna(0)
    filtered_df[fin_total_columns] = filtered_df[fin_total_columns].fillna(0)

    filtered_df[crm_qtty_columns] = filtered_df[crm_qtty_columns].fillna(0)
    filtered_df[fin_qtty_columns] = filtered_df[fin_qtty_columns].fillna(0)

    filtered_df['Cписок по CRM загалом'] = filtered_df.apply(concat_flatten_lists, columns=crm_list_columns, axis=1)
    filtered_df['Cписок по Fin загалом'] = filtered_df.apply(concat_flatten_lists, columns=fin_list_columns, axis=1)

    filtered_df['Сума по CRM загалом'] = filtered_df[crm_total_columns].sum(axis=1)
    filtered_df['Сума по Fin загалом'] = filtered_df[fin_total_columns].sum(axis=1)

    filtered_df['Кількість по CRM загалом'] = filtered_df['Cписок по CRM загалом'].apply(lambda x: len(x))
    filtered_df['Кількість по Fin загалом'] = filtered_df['Cписок по Fin загалом'].apply(lambda x: len(x))

    return filtered_df

def concat_flatten_lists(row, columns):
    concatenated_list = []
    for col in columns:
        concatenated_list.extend(row[col])
    return list(set(concatenated_list))

def find_symmetric_difference(row):
    fin_list = row['Cписок по Fin загалом']
    crm_list = row['Cписок по CRM загалом']

    # Ensure that both fin_list and crm_list are lists
    if not isinstance(fin_list, list):
        fin_list = []
    if not isinstance(crm_list, list):
        crm_list = []

    return list(set(fin_list) ^ set(crm_list))

def get_final_daily_comparison(filtered_df, _WH_needed, aggregated_WH_by_day, new_order_with_WH=new_order_with_WH, new_order_no_WH=new_order_no_WH):
    if _WH_needed:
        final_df = filtered_df.merge(aggregated_WH_by_day, how = 'outer', on = "Дата оплати")
        final_df['Замовлення в не обох списках'] = final_df.apply(lambda row: set(row['Cписок по Fin загалом'])^ set(row['Cписок по CRM загалом']), axis=1)
        df = final_df[new_order_with_WH].copy()

    else:
        final_df = filtered_df.copy()
        final_df['Замовлення в не обох списках'] = final_df.apply(lambda row: set(row['Cписок по Fin загалом'])^ set(row['Cписок по CRM загалом']), axis=1)
        df = final_df[new_order_no_WH].copy()

    return df


def compare_crm_and_WH_data(df_orders_SDD_paid, df_WH_sold_sdd, _WH_needed, cols_to_show_status_comparison=cols_to_show_status_comparison):
    if _WH_needed:
        df_orders_SDD_paid.rename(columns = {'id':'Код CRM'}, inplace=True)
        df_WH_sold_sdd['Код CRM'] = pd.to_numeric(df_WH_sold_sdd['Код CRM'])
        df_orders_SDD_paid['Код CRM'] = pd.to_numeric(df_orders_SDD_paid['Код CRM'])
        df_paid_sdd=df_orders_SDD_paid[~df_orders_SDD_paid['payment_date'].isna()].copy()
        df_by_number = df_WH_sold_sdd.merge(df_paid_sdd, how='outer', on = 'Код CRM')
        df_by_number[['Сумма', 'totalSumm']] = df_by_number[['Сумма', 'totalSumm']].fillna(0)
        df_by_number["Сумма"] = pd.to_numeric(df_by_number["Сумма"])
        df_by_number["Розбіжність по сумі"] = df_by_number["Сумма"] - df_by_number['totalSumm'] + df_by_number['delivery_cost_paid_to_us']
        df_by_number['Розбіжність по статусу'] = (df_by_number['Проведен?'] != df_by_number['status_WH']) | df_by_number['Проведен?'].isna() | df_by_number['status_WH'].isna()
        df_by_number_final = df_by_number[cols_to_show_status_comparison][(df_by_number['Розбіжність по статусу']==True)|(df_by_number['Розбіжність по сумі']!=0)]

        return df_by_number_final

    else:
        st.write("Дані для порівняння з обліком залишків не надані, порівняти неможливо.")
