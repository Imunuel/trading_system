from .models import SimpleOffer, PremiumOffer
from shares.models import Share, InventoryShare, GlobalInventory
from users.models import Inventory
from .serializers import SimpleOfferSerializer, PremiumOfferSerializer
from .models import Trade


class Checking:

    @staticmethod
    def checking_inventory_share_exists(order_type, exists, requared_count, current_count):

        if order_type == 'sell' and not exists:
            return True
        elif order_type == 'sell' and exists:
            if current_count < requared_count:
                return True



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
    global_inventory = GlobalInventory.objects.get(share=share)
    inventory_share = InventoryShare.objects.get(owner=user, share=share)

    if Checking.checking_inventory_share_exists(
        order_type=data['order_type'], 
        exists=exists, 
        requared_count=data['count'], 
        current_count=inventory_share.count):
        return False

    simple_offer = SimpleOffer.objects.create(
        user=user,
        share=share,
        count=data['count'],
        current_count=data['count'],
        order_type=data['order_type'],
        is_active=data['is_active'] 
        )
    
    inventory_share.count -= data['count']
    global_inventory.count += data['count']
    global_inventory.save()
    inventory_share.save()

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
    global_inventory = GlobalInventory.objects.get(share=share)
    inventory_share = InventoryShare.objects.get(owner=user, share=share)

    if Checking.checking_inventory_share_exists(
        order_type=data['order_type'], 
        exists=exists, 
        requared_count=data['count'], 
        current_count=inventory_share.count):
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

    inventory_share.count -= data['count']
    global_inventory.count += data['count']
    inventory_share.save()
    global_inventory.save()

    return PremiumOfferSerializer(premium_offer).data


def serialization(serializer, queryset):
    data = serializer(queryset, many=True)
    return data.data


def create_trade(share, quantity, cost, buyer, seller):
    Trade.objects.create(
        share=share,
        quantity=quantity,
        cost=cost,
        buyer=buyer,
        seller=seller
    )

def ActivateAllOffer(activate):
    if activate:
        simple_offers = SimpleOffer.objects.filter(is_active=False)
        premium_offers = PremiumOffer.objects.filter(is_active=False)

        for simple in simple_offers:
            simple.is_active = True
            simple.save()
        
        for premium in premium_offers:
            premium.is_active = True
            premium.save()
    
    if not activate:
        simple_offers = SimpleOffer.objects.filter(is_active=True)
        premium_offers = PremiumOffer.objects.filter(is_active=True)

        for simple in simple_offers:
            simple.is_active = False
            simple.save()
        
        for premium in premium_offers:
            premium.is_active = False
            premium.save()