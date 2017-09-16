# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 20:12:20 2017

@author: erlendvollset
"""

import requests

def main():
    customer1 = get_customer('19078984062')
    print(customer1["firstName"], customer1["personalNumber"])


def get_customer(customerId):
    url = "https://dnbapistore.com/hackathon/customers/1.0/customer/{}".format(customerId)
    headers = {'Authorization': 'Bearer d018eb95-ff43-3314-a8d6-55696f9ba202', 'Accept': 'application/json'}
    r = requests.get(url, headers=headers)
    d = r.json()
    return d

def get_account_overview():
    print("hello")



if __name__ == "__main__":
    main()