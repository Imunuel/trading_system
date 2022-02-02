from django.contrib.auth import get_user_model

from .models import Inventory

User = get_user_model()


def create_user(data):
    return User.objects.create(**data)


def change_balans(owner, data):
    inventory = Inventory.objects.get(owner=owner)
    inventory.balans += data['balans']
    inventory.save()

    if data['premium'] and inventory.balans >= 100 and inventory.premium is False:
        inventory.premium = True
        inventory.balans -= 100
        inventory.save()
        data = {
            'balans': inventory.balans,
            'premium': inventory.premium
        }
        return data
    
    elif data['premium'] and inventory.premium:
        inventory.save()
        data = {
            'balans': inventory.balans,
            'premium': inventory.premium
        }
        return data

    elif data['premium'] and inventory.balans < 100 and inventory.premium is False:
        inventory.save()
        return False

    data = {
            'balans': inventory.balans,
            'premium': inventory.premium
        }
    return data