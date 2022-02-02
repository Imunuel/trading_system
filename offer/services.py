from .models import SimpleOffer, PremiumOffer
from shares.models import Share
from .serializers import SimpleOfferSerializer, PremiumOfferSerializer


def create_simple_offer(user, data):
    share = Share.objects.get(name=data['share']['name'])
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
    share = Share.objects.get(name=data['share']['name'])
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