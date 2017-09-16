from django.shortcuts import render, redirect
from django.http import HttpResponse
from splitter.apps.api import dnb as dnb_api
from splitter.apps.controller.splitcontrol import SplitterController
from .models import UserProfile, Transaction
from splitter.apps.group.models import Group

def index(request):
    ctr = SplitterController()
    cid = '23088983723'
    user = UserProfile.objects.get(customer_id=cid)

    main_user_transactions = ctr.get_user_transactions(user_id=user.customer_id)
    # accounts = dnb_api.get_accounts('07066363656')
    someone = ctr.get_user(user_id='07066363656')
    return HttpResponse("<h3>{0}</h3>".format(user.user.get_full_name()))

    #TODO: Get necessary information to view
