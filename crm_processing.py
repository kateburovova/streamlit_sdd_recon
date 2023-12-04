import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, timedelta
import time
import json
import numpy as np
import io
import pytz

from dicts import shipmentStores

cred_api_url = st.secrets['crm']['cred_api_url']
cred_crm_api_key = st.secrets['crm']['cred_crm_api_key']

def get_payment_types_dict(api_url=cred_api_url, api_key=cred_crm_api_key, page=1):
    endpoint = f"{api_url}/api/v5/reference/payment-types"
    params = {
        "apiKey": api_key
    }

    try:
        response = requests.get(endpoint, params=params)
        response_data = response.json()

        if response_data.get("success"):
            return pd.DataFrame(response_data.get("paymentTypes", [])).to_dict()
        else:
            return "Error in API response: " + str(response_data.get("errorMsg"))
    except Exception as e:
        return "Error in making API request: " + str(e)


def get_order_statuses_dict(api_url=cred_api_url, api_key=cred_crm_api_key, page=1):

    endpoint = f"{api_url}/api/v5/reference/statuses"
    params = {
        "apiKey": api_key
    }

    try:
        response = requests.get(endpoint, params=params)
        response_data = response.json()

        if response_data.get("success"):
            return pd.DataFrame(response_data.get("statuses", [])).to_dict()
        else:
            return "Error in API response: " + str(response_data.get("errorMsg"))
    except Exception as e:
        return "Error in making API request: " + str(e)

def get_one_page_inventory(store, api_url=cred_api_url, api_key=cred_crm_api_key, page=1):
    endpoint = f"{api_url}/api/v5/store/inventories"
    params = {
        "apiKey": api_key,
        'page': page
    }

    try:
        response = requests.get(endpoint, params=params)
        response_data = response.json()

        if response_data.get("success"):
          return response_data.get("offers", [])
            # return pd.DataFrame(response_data.get("offers", [])).to_dict()
        else:
            return "Error in API response: " + str(response_data.get("errorMsg"))
    except Exception as e:
        return "Error in making API request: " + str(e)


def get_page_count_inventory(store, api_url=cred_api_url, api_key=cred_crm_api_key):
    """
    Retrieves the total page count of inventory data from a specified store using API.

    This function makes an API call to the inventory endpoint and retrieves
    the total number of pages of inventory data for a given store.

    Args:
        store (str): A key representing the store for which inventory data is needed.
                     Currently supports 'sdd' and 'u8' as valid keys.
        api_url (str, optional): The base URL of the API.
        api_key (str, optional): The API key used for authenticating with the CRM                                 Defaults to a predetermined API key.

    Returns:
        int or str: The total number of pages in the inventory data if the API call is successful.
                    If there's an error in the API response or in making the API request,
                    a descriptive error message string is returned.
    """
    sites = {'sdd':'000000002',
             'u8':'000000001'}

    endpoint = f"{api_url}/api/v5/store/inventories"
    params = {
        "apiKey": api_key,
        'filter[sites][]': [sites[store]],
        'filter[productActive]': 1

    }

    try:
        response = requests.get(endpoint, params=params)
        response_data = response.json()

        if response_data.get("success"):
            pagination_info = response_data.get("pagination", {})
            total_pages = pagination_info.get("totalCount", 0)
            return total_pages
        else:
            return "Error in API response: " + str(response_data.get("errorMsg"))
    except Exception as e:
        return "Error in making API request: " + str(e)


def get_inventory_info_dict_by_id(store, id, api_url=cred_api_url, api_key=cred_crm_api_key, page=1):
    endpoint = f"{api_url}/api/v5/store/inventories"
    params = {
        "apiKey": api_key,
        'filter[ids][]' : id
    }

    try:
        response = requests.get(endpoint, params=params)
        response_data = response.json()

        if response_data.get("success"):
            return pd.DataFrame(response_data.get("offers", [])).to_dict()
        else:
            return "Error in API response: " + str(response_data.get("errorMsg"))
    except Exception as e:
        return "Error in making API request: " + str(e)


def get_product_info_dict_by_id(store, id, api_url=cred_api_url, api_key=cred_crm_api_key):
    '''
    example get_product_info_dict_by_id('sdd', '132420')
    '''
    endpoint = f"{api_url}/api/v5/store/products"
    params = {
        "apiKey": api_key,
        'filter[ids][]' : id
    }

    try:
        response = requests.get(endpoint, params=params)
        response_data = response.json()

        if response_data.get("success"):
            return pd.DataFrame(response_data.get("products", [])).to_dict()
        else:
            return "Error in API response: " + str(response_data.get("errorMsg"))
    except Exception as e:
        return "Error in making API request: " + str(e)

def get_one_page_products(store, api_url=cred_api_url, api_key=cred_crm_api_key, page=1):
    endpoint = f"{api_url}/api/v5/store/products"
    params = {
        "apiKey": api_key,
        'page': page
    }

    try:
        response = requests.get(endpoint, params=params)
        response_data = response.json()

        if response_data.get("success"):
          return response_data.get("products", [])
        else:
            return "Error in API response: " + str(response_data.get("errorMsg"))
    except Exception as e:
        return "Error in making API request: " + str(e)


def get_page_count_products(store, api_url=cred_api_url, api_key=cred_crm_api_key):

    sites = {'sdd':'000000002',
             'u8':'000000001'}

    endpoint = f"{api_url}/api/v5/store/products"
    params = {
        "apiKey": api_key,
        'filter[sites][]': [sites[store]]
        }

    try:
        response = requests.get(endpoint, params=params)
        response_data = response.json()

        if response_data.get("success"):
            pagination_info = response_data.get("pagination", {})
            total_pages = pagination_info.get("totalCount", 0)
            return total_pages
        else:
            return "Error in API response: " + str(response_data.get("errorMsg"))
    except Exception as e:
        return "Error in making API request: " + str(e)

def get_all_inventory(store, api_url=cred_api_url, api_key=cred_crm_api_key):

  total_pages = get_page_count_inventory(store)
  all_inventory = []

  for page in range(1, total_pages + 1):
    page_iventory = get_one_page_inventory(store, api_url, api_key, page)
    if isinstance(page_iventory, list):
        all_inventory.extend(page_iventory)
    else:
        print(f"Error fetching page {page}: {page_iventory}")

  df_inventory = pd.DataFrame(all_inventory)
  return df_inventory

def get_all_products(store, api_url=cred_api_url, api_key=cred_crm_api_key):

  total_pages = get_page_count_products(store)
  all_products = []

  for page in range(1, total_pages + 1):
    page_products = get_one_page_products(api_url, api_key, page)
    if isinstance(page_products, list):
        all_products.extend(page_products)
    else:
        print(f"Error fetching page {page}: {page_products}")

  df_products = pd.DataFrame(all_products)
  return df_products

def get_one_page_of_CRM_orders(api_url=cred_api_url, api_key=cred_crm_api_key, page=1):
    """
    Fetches orders from CRM.

    :param api_url: Base URL for the CRM API.
    :param api_key: Your CRM API key.
    :param page: Page number for pagination (default is 1).

    :return: List of orders or an error message.
    """
    endpoint = f"{api_url}/api/v5/orders"
    params = {
        "apiKey": api_key,
        "page": page
    }

    try:
        response = requests.get(endpoint, params=params)
        response_data = response.json()

        if response_data.get("success"):
            return response_data.get("orders", [])
        else:
            return "Error in API response: " + str(response_data.get("errorMsg"))
    except Exception as e:
        return "Error in making API request: " + str(e)

def get_page_count(start_date, end_date, api_url=cred_api_url, api_key=cred_crm_api_key):
    """
    Fetches the total number of pages of orders within a specified date range from CRM.

    :param api_url: Base URL for the CRM API.
    :param api_key: Your CRM API key.
    :param start_date: Start date for the order range (format: 'YYYY-MM-DD').
    :param end_date: End date for the order range (format: 'YYYY-MM-DD').

    :return: Total number of pages or an error message.
    """
    endpoint = f"{api_url}/api/v5/orders"
    params = {
        "apiKey": api_key,
        "filter[createdAtFrom]": start_date,
        "filter[createdAtTo]": end_date,
        "page": 1
    }

    try:
        response = requests.get(endpoint, params=params)
        response_data = response.json()

        if response_data.get("success"):
            pagination_info = response_data.get("pagination", {})
            total_pages = pagination_info.get("totalPageCount", 0)
            return total_pages
        else:
            return "Error in API response: " + str(response_data.get("errorMsg"))
    except Exception as e:
        return "Error in making API request: " + str(e)


def get_all_orders_from_timesteps(start_date, end_date, api_url=cred_api_url, api_key=cred_crm_api_key):
  total_pages = get_page_count(api_url, api_key, start_date, end_date)
  all_orders = []

  for page in range(1, total_pages + 1):
    page_orders = get_one_page_of_CRM_orders(api_url, api_key, page)
    if isinstance(page_orders, list):
        all_orders.extend(page_orders)
    else:
        print(f"Error fetching page {page}: {page_orders}")

  df_orders = pd.DataFrame(all_orders)
  custom_fields_df = pd.json_normalize(df_orders['customFields'])
  df_orders = df_orders.join(custom_fields_df)
  df_orders.drop('customFields', axis=1, inplace=True)

  return df_orders

def assign_store(shipment_store_code, shipmentStores=shipmentStores):
    store_name = shipmentStores.get(shipment_store_code, "")
    if 'U8' in store_name:
        return 'U8'
    elif 'SDD' in store_name:
        return 'SLASHDOTDASH'
    else:
        return None
def extract_data_from_items(row, dataname):
    if row['items'] and isinstance(row['items'], list):
        return row['items'][0].get(dataname, 0)
    return 0

def extract_payment_status(payment_info):
    if payment_info and isinstance(payment_info, dict):
        first_key = next(iter(payment_info))
        return payment_info[first_key].get('status')
    else:
        return None

def extract_payment_type(payment_info):
    if payment_info and isinstance(payment_info, dict):
        first_key = next(iter(payment_info))
        return payment_info[first_key].get('type')
    else:
        return None

def extract_payment_datetime(payment_info):
    if payment_info and isinstance(payment_info, dict):
        first_key = next(iter(payment_info))
        return payment_info[first_key].get('paidAt')
    else:
        return None

def extract_delivery_cost(delivery_info):
    if isinstance(delivery_info, dict) and 'cost' in delivery_info:
        return delivery_info['cost']
    return None

def extract_display_names(row):
    display_names = []

    for item in row.get('items', []):
        if 'offer' in item and 'displayName' in item['offer']:
            display_names.append(item['offer']['displayName'])

    return display_names

def extract_delivery_netCost(delivery_info):
    if isinstance(delivery_info, dict) and 'cost' in delivery_info:
        return delivery_info['netCost']
    return None

def extract_payment_comment(payment_info):
    if payment_info and isinstance(payment_info, dict):
        first_key = next(iter(payment_info))
        return payment_info[first_key].get('comment')
    else:
        return None

def sum_discounts(row):
    total_discount = 0

    if row['items'] and isinstance(row['items'], list):
        for item in row['items']:
            total_discount += item.get('discountTotal', 0)

    return total_discount

def sum_total_items_price_before_discount(row):
    total_discount = 0

    if row['items'] and isinstance(row['items'], list):
        for item in row['items']:
            total_discount += item.get('initialPrice', 0)

    return total_discount

def get_timeframe(start_date, end_date):

    start_date_ = datetime.strptime(start_date, '%Y-%m-%d')
    end_date_ = datetime.strptime(end_date, '%Y-%m-%d')
    start_date_utc = datetime.combine(start_date, datetime.min.time())-timedelta(days=30)
    start_date_utc_normal = datetime.combine(start_date, datetime.min.time())
    end_date_utc = datetime.combine(end_date, datetime.max.time())

    return (start_date_utc, start_date_utc_normal, end_date_utc)