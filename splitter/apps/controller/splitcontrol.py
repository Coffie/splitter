# !/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 15 02:12:20 2017

@author: erlendvollset
"""

from splitter.apps.group.models import Group
from splitter.apps.userprofile.models import UserProfile, Transaction
# import util.helpers as helpers
import splitter.apps.util.helpers as helpers

# from api import dnb as dnb_api
import splitter.apps.api.dnb as dnb_api
from splitter.apps.ml.transaction_classifier import Classifier
# from transaction_classifier import Classifier

class SplitterController:
    def __init__(self):
        self.clf = Classifier()

    def get_group(self, group_id):
        return Group.objects.get(group_id=group_id)

    def get_user(self, user_id):
        return UserProfile.objects.get(customer_id=user_id)

    def get_all_users_in_group(self, group_id):
        group = self.get_group(group_id)
        return [u for u in UserProfile.objects.filter(group)]

    def get_user_transactions(self, user_id):
        user = self.get_user(user_id)
        transactions = [t for t in Transaction.objects.filter(customer_id=user)]
        return transactions

    def get_group_relevant_transactions(self, group_id):
        transactions = []
        group = Group.objects.get(group_id=group_id)
        users = UserProfile.objects.filter(group=group)
        for user in users:
            user_transactions = self.get_user_transactions(user.customer_id)
            transactions.extend([t for t in user_transactions if (t.relevant and group.created < t.timestamp)])
        return transactions

    def transfer_money(self, sender_account_num, receiver_account_num, amount, message):
        dnb_api.transfer_funds(sender_account_num=sender_account_num,
                               receiver_account_num=receiver_account_num,
                               message=message,
                               amount=amount)

    def make_card_payment(self, user_id, amount, message):
        user = self.get_user(user_id)
        dnb_api.make_card_payment(sender_account_num=user.account_id, amount=amount, message=message)
        if self.clf.predict([message]):
            other_users = self.get_all_users_in_group(user.group.group_id)
            for other_user in other_users:
                if user != other_user:
                    self.transfer_money(user.account_id,
                                        other_user.account_id,
                                        str(float(amount) / len(other_users)),
                                        "Tilbakebetaling til {}".format(user.username))
        self.update_data()


    def update_data(self):
        # update database with data from api
        groups = Group.objects.all()
        for group in groups:
            users = self.get_all_users_in_group(group.group_id)
            for user in users:
                new_transactions = dnb_api.get_transactions(user.user_id, user.account_id, group.last_updated, helpers.get_date_now())
                old_transactions = self.get_user_transactions(user.user_id)
                for t in new_transactions:
                    if t["transactionID"] not in [t.transaction_id for t in old_transactions]:
                        new_transaction = Transaction(transaction_id=t["transactionId"],
                                                      customer=user,
                                                      timestamp=t["timeStamp"],
                                                      amount=t["amount"],
                                                      description=t["Message/kid"],
                                                      relevant=self.clf.predict([t["Message/kid"]])[0])
                        new_transaction.save()
            group.last_updated = helpers.get_date_now()

def main():
    controller = SplitterController()

    customer_id = '19078984062'
    start_date = '01012017'
    end_date = '17092017'

    # get customer
    customer1 = dnb_api.get_customer(customer_id)
    print("Customer: ", customer1["firstName"], customer1["personalNumber"], customer1["customerID"])

    # get first account
    accounts = dnb_api.get_accounts(customer_id)
    first_account = accounts[0]
    print("Primary Account: ", first_account)

    # make new payment
    dnb_api.make_card_payment(first_account["accountNumber"], "300", "Rema1000")

    # get all transactions for first account
    transactions = dnb_api.get_transactions(customer_id, first_account["accountNumber"], start_date, end_date)
    for t in transactions:
        print(t)
    transaction_texts = [t["message/KID"] for t in transactions]
    print("\nTransactions ")
    predictions = controller.clf.predict(transaction_texts)

    # print transactions and labels
    for t in zip(transactions, predictions):
        prediction = t[1]
        if prediction == '1':
            print("Description: {}".format(t[0]["message/KID"]))
            print("Amount: {}".format(t[0]["amount"]))
            print("Label: {}".format("Food" if t[1] == '1' else 'Other'))
            print()

if __name__ == "__main__":
    main()
