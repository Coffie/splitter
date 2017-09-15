# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 20:12:20 2017

@author: erlendvollset
"""

class Transaction:
    def __init__(self, transactionId, description, amount):
        self.id = transactionId
        self.description = description
        self.amount = amount

    #TODO: getters, setters ++