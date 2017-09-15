# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 20:12:20 2017

@author: erlendvollset
"""

class Account:
    def __init__(self, accountId, account_name, ):
        self.id = accountId
        self.name = account_name
        # List of groups
        self.transactions = []


        # TODO: getters, setters, get_relevant transactions (ml)
