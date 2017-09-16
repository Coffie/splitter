from __future__ import unicode_literals

from django.db import models

class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    last_updated = models.DateField()
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

