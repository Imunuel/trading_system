from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from users.models import Inventory
from offer.models import SimpleOffer, PremiumOffer, Trade
from shares.models import Share

User = get_user_model()

@transaction.atomic
@receiver(post_save, sender=User)
def create_inventory(sender, instance, created, *args, **kwargs):
    if created:
        Inventory.objects.create(owner=instance)


@receiver(post_save, sender=SimpleOffer)
def search_buy_simple_offer(sender, instance, *args, **kwargs):
    if instance.order_type == 'sell' and instance.is_active:
        simple_offers = SimpleOffer.objects.filter(order_type='buy', share=instance.share, is_active=True)
        share = instance.share

        for buy_offer in simple_offers:

            _min_count_offer = min(instance.current_count, buy_offer.current_count)
            _min_price_offer = share.current_price * _min_count_offer #500
            
            buy_price = buy_offer.user.inventory // share.current_price #5



            buy_offer.current_count -= _min_count
            instance.current_count -= _min_count

            if instance.current_count == 0:
                instance.is_active = False
            
            if buy_offer.current_count == 0:
                buy_offer.is_active = False

            buy_offer.save()
            instance.save()


@receiver(post_save, sender=SimpleOffer)
def search_sell_simple_offer(sender, instance, *args, **kwargs):
    if instance.order_type == 'buy' and instance.is_active:
        simple_offers = SimpleOffer.objects.filter(order_type='sell', share=instance.share, is_active=True)

        for sell_offer in simple_offers:

            _min_count = min(instance.current_count, sell_offer.current_count)

            sell_offer.current_count -= _min_count
            instance.current_count -= _min_count

            if instance.current_count == 0:
                instance.is_active = False
            
            if sell_offer.current_count == 0:
                sell_offer.is_active = False

            sell_offer.save()
            instance.save()