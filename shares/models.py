from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Share(models.Model):
    name = models.CharField(max_length=5)
    full_name = models.CharField(max_length=255)
    current_price = models.IntegerField(default=0)
    past_price = models.IntegerField(default=0)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class InventoryShare(models.Model):
    owner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='InventoryShare')
    share = models.ForeignKey(Share, blank=True, null=True, on_delete=models.SET_NULL, related_name='share')
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ('owner', 'share')

    def __str__(self):
        return f'{self.owner} {self.share.name} {self.count}'


class GlobalInventory(models.Model):
    share = models.ForeignKey(Share, blank=True, null=True, on_delete=models.SET_NULL, related_name='global_share')
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ('share',)

    def __str__(self):
        return f'{self.share} {self.count}'