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
    members = ctr.get_all_users_in_group(group_id=group.group_id)
    transaction_list = []
    for member in members:
        if member.customer_id != user.customer_id:
            transaction_list.append(get_user_list_transactions(member.customer_id))

    group_transactions = ctr.get_group_relevant_transactions(group.group_id)
    total_group_expense = 0.0
    for trans in group_transactions:
        total_group_expense += float(trans.amount)

    main_user_transactions = ctr.get_user_transactions(user_id=user.customer_id)[-9:]
    transactions = make_message_readable(main_user_transactions)

    balance = ctr.get_primary_account_balance(user_id=user.customer_id)


    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            amount = request.POST['amount']
            message = request.POST['message']
            ctr.make_card_payment(user_id=user.customer_id, amount=amount, message=message)
            transactions = ctr.get_user_transactions(user_id=user.customer_id)[-9:]
            transactions = make_message_readable(transactions)
            balance = ctr.get_primary_account_balance(user_id=user.customer_id)
            total_group_expense += float(amount)
            member_list = get_member_lists(group, user.customer_id)
            trans_list = []
            for member in members:
                if member.customer_id != user.customer_id:
                    trans_list.append(get_user_list_transactions(member.customer_id))

            
            context = {
                    'transactions': transactions,
                    'group': group,
                    'user': user,
                    'balance': balance,
                    'form': form,
                    'total_group_expense': total_group_expense,
                    'transaction_list': trans_list,

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
                'total_group_expense': total_group_expense,
                'transaction_list': transaction_list,
                }

        return render(request, 'userprofile/index.html', context)

    
def make_message_readable(transactions):
    transactions = list(reversed(transactions))
    for transaction in transactions:
        desc = ""
        desc += transaction.description[:14] + "..."
        transaction.description = desc
    return transactions

def get_user_list_transactions(user_id):
    ctr = SplitterController()
    transactions = ctr.get_user_transactions(user_id=user_id)[-9:]
    transactions = make_message_readable(transactions)
    return transactions

def get_member_lists(group, sender):
    ctr = SplitterController()
    group_members = ctr.get_all_users_in_group(group_id=group.group_id)
    member_list = []
    for member in group_members:
        if member.customer_id == sender:
            continue
        member_list.append(get_user_list_transactions(member.customer_id))
    return member_list

        
    

