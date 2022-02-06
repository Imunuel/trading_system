from .models import SimpleOffer, PremiumOffer
from shares.models import Share, InventoryShare
from users.models import Inventory
from .serializers import SimpleOfferSerializer, PremiumOfferSerializer


def create_simple_offer(user, data):
    '''
    data = {
        'share',
        'count',
        'order_type',
        'is_active'
    }
    '''
    share = Share.objects.get(name=data['share']['name'])
    exists = InventoryShare.objects.filter(owner=user, share=share).exists()

    if data['order_type'] == 'sell' and not exists:
        return False
    elif data['order_type'] == 'sell' and exists:
        inventory_share = InventoryShare.objects.get(owner=user, share=share).count
        if inventory_share < data['count']:
            return False

    simple_offer = SimpleOffer.objects.create(
        user=user,
        share=share,
        count=data['count'],
        current_count=data['count'],
        order_type=data['order_type'],
        is_active=data['is_active'] 
        )
    return SimpleOfferSerializer(simple_offer).data


def create_premium_offer(user, data):
    '''
    data = {
        'share',
        'count',
        'price',
        'order_type',
        'is_active'
    }
    '''
    share = Share.objects.get(name=data['share']['name'])
    exists = InventoryShare.objects.filter(owner=user, share=share).exists()

    if data['order_type'] == 'sell' and not exists:
        return False
    elif data['order_type'] == 'sell' and exists:
        inventory_share = InventoryShare.objects.get(owner=user, share=share).count
        if inventory_share < data['count']:
            return False

    premium_offer = PremiumOffer.objects.create(
        user=user,
        share=share,
        count=data['count'],
        current_count=data['count'],
        price=data['price'],
        order_type=data['order_type'],
        is_active=data['is_active'] 
        )
    
    return PremiumOfferSerializer(premium_offer).data


def serialization(serializer, queryset):
    data = serializer(queryset, many=True)
    return data.data