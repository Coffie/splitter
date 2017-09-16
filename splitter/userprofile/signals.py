from django.db.models.signals import post_save
from django.dispatch import reciever
from .models import UserProfile
from django.contrib.auth import User

@reciever(post_save, sender=User)
def create_user_profile(sender, **kwargs):
    user = kwargs['instance']
    customer_id = kwargs['customer_id']
    account_id = kwargs['account_id']

    up = UserProfile(customer_id=customer_id, user=user, account_id=account_id)
    up.save()
