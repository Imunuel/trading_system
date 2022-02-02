from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

from .models import Share, InventoryShare
from users.models import Inventory

User = get_user_model()


def buy_shares(user:User, share:Share(), count:int):
    current_chare = Share.objects.get(name=share.name) #интересующая нас акция
    price = current_chare.current_price #текущая стоимость акции
    total_price = price*count #стоимость покупки
    invetory = Inventory.objects.get(owner=user) #инвентарь пользователя с балансом

    if invetory.balans < total_price:
        return False

    inventory_share = InventoryShare.objects.get_or_create(owner=user, share=share) #определенная акция в инвентаре пользователя
    Inventory.balans -= total_price
    inventory_share.count = count #количество купленных акций
    return True
    