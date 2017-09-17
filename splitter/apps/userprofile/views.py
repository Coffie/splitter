from django.shortcuts import render, redirect
from django.http import HttpResponse
from splitter.apps.api import dnb as dnb_api
from splitter.apps.controller.splitcontrol import SplitterController
from .models import UserProfile, Transaction
from splitter.apps.group.models import Group
from .forms import PaymentForm

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

    # ctr.update_data()
    main_user_transactions = ctr.get_user_transactions(user_id=user.customer_id)
    # accounts = dnb_api.get_accounts('07066363656')
    someone = ctr.get_user(user_id='07066363656')
    balance = ctr.get_primary_account_balance(user_id=user.customer_id)


    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = request.POST['amount']
            message = request.POST['description']
            ctr.make_card_payment(user_id=user.customer_id, amount=amount, message=message)
            transactions = ctr.get_user_transactions(user_id=user.customer_id)[-9:]
            transactions = list(reversed(transaction))
            for transaction in transactions:
                desc = ""
                desc += transaction.description[:14] + "..."
                transaction.description = desc
            balance = ctr.get_primary_account_balance(user_id=user.customer_id)
            
            context = {
                    'transactions': transactions,
                    'group': group,
                    'user': user,
                    'balance': balance,
                    'form': form,
                    }
            return render(request, 'userprofile/index.html', context)
                    

    else:
        form = PaymentForm()
        context = {
                'transactions': transactions,
                'group': group,
                'group_transactions': group_transactions,
                'user': user,
                'balance': balance,
                'form': form,
                }

        return render(request, 'userprofile/index.html', context)

    
def make_message_readable(transactions):
    text = []
    for transaction in transactions:
        desc = ""
        desc += transaction.description[:14] + "..."
        transaction.description = desc
    return transactions

