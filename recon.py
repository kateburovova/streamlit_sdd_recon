import pandas as pd
import requests
import time
import json
import numpy as np
import pytz
from google.oauth2.service_account import Credentials
import gspread

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


