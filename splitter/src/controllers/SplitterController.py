# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 02:12:20 2017

@author: erlendvollset
"""

from api import dnb as dnb_api


def main():
    customerId = 19078984062
    customer = dnb_api.get_customer(customerId)
    for attr in customer.items():
        print(attr)



if __name__ == "__main__":
    main()
