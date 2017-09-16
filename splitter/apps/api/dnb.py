# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 20:12:20 2017

@author: erlendvollset
"""

import requests
# import util.helpers as helpers
import splitter.apps.util.helpers as helpers
import json

API_KEY = "d018eb95-ff43-3314-a8d6-55696f9ba202"


# General get and put methods
def get(url):
    headers = {'Authorization': 'Bearer {}'.format(API_KEY), 'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    return r.json()


def put(url, body):
    headers = {'Authorization': 'Bearer {}'.format(API_KEY), 'Accept': 'application/json'}
    r = requests.put(url, headers=headers)
    return r.json()

# Specific API endpoint calls
def get_customer(customer_id):
    url = "https://dnbapistore.com/hackathon/customers/1.0/customer/{}".format(customer_id)
    customer = get(url)
    return customer

def get_accounts(customerId):
    url = "https://dnbapistore.com/hackathon/accounts/1.0/account/customer/{}".format(customerId)
    accounts_overview = get(url)
    return accounts_overview['accounts']

def get_transactions(customer_id, account_number, date_from, date_to):
    url= "https://dnbapistore.com/hackathon/accounts/1.0/account?accountNumber={}&customerID={}&dateFrom={}&dateTo={}"\
        .format(account_number, customer_id, date_from, date_to)
    transaction_details = get(url)
    return transaction_details['transactions']

def transfer_funds(sender_account_num, receiver_account_num, message, amount):
    url = "https://dnbapistore.com/hackathon/payments/1.0/payment"
    body = {
        "debitAccountNumber": str(sender_account_num),
        "creditAccountNumber": str(receiver_account_num),
        "message": message,
        "amount": str(amount),
        "paymentDate": helpers.get_date_now()
    }
    response = put(url, json.dumps(body))
    return response["paymentStatus"], response["paymentIDNumber"]

def make_card_payment(sender_account_num, amount, message):
    url = "https://dnbapistore.com/hackathon/payments/1.0/payment/card"
    body = {
        "debitAccountNumber": str(sender_account_num),
        "message": message,
        "amount": str(amount),
        "paymentDate": helpers.get_date_now()
    }
    print(json.dumps(body))
    # response = put(url, json.dumps(body))
    # print(response)
    # return response["paymentStatus"], response["paymentIDNumber"]



