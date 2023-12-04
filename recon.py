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
    # df_discounts_merged_nonzero = df_discounts_merged_clean[df_discounts_merged_clean['diff']!=0]

    # return df_discounts_merged_nonzero
    return df_discounts_merged_clean

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





