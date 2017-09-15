# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 20:12:20 2017

@author: erlendvollset
"""

class SplitterGroup:
    def __init__(self, groupId, members):
        self.id = groupId
        self.num_members = len(members)
        self.members = members


