from django.db import models
from django.contrib.auth.models import User


class Inventory(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    balans = models.IntegerField(default=0)
    premium = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.owner} {self.balans} {self.premium}' 
