from django.db import models

class UserProfile(models.Model):
    debitAccountNumber = models.IntegerField()

