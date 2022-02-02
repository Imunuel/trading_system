from django.db import models
from django.contrib.auth.models import User


class Inventory(models.Model):
    owner = models.ForeignKey(User, on_delete=models.PROTECT)
    balans = models.IntegerField(default=0)

    def __str__(self):
        return self.owner.username
