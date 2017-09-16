# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 20:12:20 2017

@author: erlendvollset
"""

class User:
    def __init__(self, customerId, firstName, lastName, accountId, group_id = None):
        self.id = customerId
        self.name = (firstName, lastName)
        self.account_id = accountId
        # List of groups
        self.group_id = group_id
        # List of transactions
        self.transactions = []

    def get_relevent_transactions(customerId, transactions):
        print("hello relevant transactions")

        # TODO: getters, setters, get_relevant transactions (ml)

        # TODO: getters, setters, accounts