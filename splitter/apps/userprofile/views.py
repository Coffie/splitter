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
    name = user.user.get_full_name()
    group = ctr.get_group(user.group_id)
    group_transactions = ctr.get_group_relevant_transactions(group.group_id)

    main_user_transactions = ctr.get_user_transactions(user_id=user.customer_id)[-9:]
    transactions = list(reversed(main_user_transactions))
    for transaction in transactions:
        desc = ""
        desc += transaction.description[:14] + "..."
        transaction.description = desc

    # accounts = dnb_api.get_accounts('07066363656')
    someone = ctr.get_user(user_id='07066363656')

    context = {
            'transactions': transactions,
            'group': group,
            'group_transactions': group_transactions,
            'user': user,
            }

    return render(request, 'userprofile/index.html', context)

    


    #TODO: Get necessary information to view
