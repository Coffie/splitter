from django.db import models
from django.contrib.auth.models import User
from splitter.apps.group.models import Group

class UserProfile(models.Model):
    customer_id = models.BigIntegerField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    account_id = models.BigIntegerField()
    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.get_full_name()
    
class Transaction(models.Model):
    transaction_id = models.BigIntegerField(primary_key=True)
    customer = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    amount = models.BigIntegerField()
    description = models.CharField(max_length=200)
    relevant = models.BooleanField(default=False)


