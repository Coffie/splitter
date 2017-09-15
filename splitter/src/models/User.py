# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 20:12:20 2017

@author: erlendvollset
"""

class User:
    def __init__(self, customerId, firstName, lastName):
        self.id = customerId
        self.name = (firstName, lastName)

        # List of groups
        self.groups = []

    # TODO: getters, setters, accounts