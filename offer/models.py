from django.db import models
from django.contrib.auth.models import User

from shares.models import Share


ORDER_TYPE = (('buy', 'Buy'), ('sell', 'Sell'))

class SimpleOffer(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    share = models.ForeignKey(Share, blank=True, null=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=0)
    current_count = models.IntegerField(default=0)

    order_type = models.CharField(max_length=4, choices=ORDER_TYPE)
    is_active = models.BooleanField()

    def __str__(self):
        return f'{self.user} {self.order_type} {self.is_active}'


class PremiumOffer(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    share = models.ForeignKey(Share, blank=True, null=True, on_delete=models.SET_NULL)
    count = models.IntegerField(default=0)
    current_count = models.IntegerField(default=0)
    price = models.IntegerField(default=0)

    order_type = models.CharField(max_length=4, choices=ORDER_TYPE)
    is_active = models.BooleanField()

    def __str__(self):
        return f'{self.user} {self.order_type} {self.is_active}'

class Trade(models.Model):
    share = models.ForeignKey(Share, blank=True, null=True, on_delete=models.SET_NULL)
    quantity = models.IntegerField(default=0)
    cost = models.IntegerField(default=0)

    buyer = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='buyer')
    seller = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name='seller')
    
    buyer_offer = models.CharField(max_length=255)
    seller_offer = models.CharField(max_length=255)

    def __str__(self):
        return f'buyer: {self.buyer} \ seller: {self.seller}'