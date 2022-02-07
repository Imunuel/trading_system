from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

from users.models import Inventory
from offer.models import SimpleOffer, PremiumOffer, Trade
from shares.models import Share, InventoryShare, GlobalInventory
from offer.services import create_trade

User = get_user_model()


class SignalsAfterCreation:

    @transaction.atomic
    @receiver(post_save, sender=User)
    def create_inventory(sender, instance, created, *args, **kwargs):
        if created:
            Inventory.objects.create(owner=instance)

    @transaction.atomic
    @receiver(post_save, sender=SimpleOffer)
    def create_inventory_share_after_creation_offer(sender, instance, created, *args, **kwargs):
        if created and instance.order_type == 'buy':
            if InventoryShare.objects.filter(owner=instance.user, share=instance.share).exists():
                return True
            InventoryShare.objects.create(owner=instance.user, share=instance.share)

    @transaction.atomic
    @receiver(post_save, sender=Share)
    def create_global_inventory_after_creation_share(sender, instance, created, *args, **kwargs):
        if created:
            GlobalInventory.objects.create(share=instance, count=500)


@transaction.atomic
def creation_trade_using_offers(buyer_inventory_share, 
                                buyer_inventory, 
                                seller_inventory, 
                                buyer_offer, 
                                seller_offer, 
                                global_inventory, 
                                share):
    
    # --------------------------- математические вычисления -------------------------------------
    _min_count_offer = min(buyer_offer.current_count, seller_offer.current_count)
    _min_price_offer = share.current_price * _min_count_offer 
    _min_buy_price_offer = min(_min_price_offer, buyer_inventory.balans) 

    _share_count_in_trade = _min_buy_price_offer // share.current_price
    _total_price_in_trade = _share_count_in_trade * share.current_price
    # ----------------------------------------------------------------------------------------------

    if _share_count_in_trade > 0:

        buyer_offer.current_count -= _share_count_in_trade
        seller_offer.current_count -= _share_count_in_trade

        if seller_offer.current_count == 0:
            seller_offer.is_active = False
                    
        if buyer_offer.current_count == 0:
            buyer_offer.is_active = False

        buyer_inventory_share.count += _share_count_in_trade
        buyer_inventory.balans -= _total_price_in_trade
        seller_inventory.balans += _total_price_in_trade
        global_inventory.count -= _share_count_in_trade

        create_trade(
            share=share, 
            quantity=_share_count_in_trade, 
            cost=_total_price_in_trade, 
            buyer=buyer_offer.user, 
            seller=seller_offer.user
            )

        buyer_inventory_share.save()
        buyer_inventory.save()
        seller_inventory.save()
        buyer_offer.save()
        seller_offer.save()
        global_inventory.save()


@transaction.atomic
@receiver(post_save, sender=SimpleOffer)
def trading_by_simple_offer(sender, instance, *args, **kwargs):
    share = instance.share
    global_inventory = GlobalInventory.objects.get(share=share)

    if instance.order_type == 'sell' and instance.is_active:

        simple_offers = SimpleOffer.objects.filter(order_type='buy', share=share, is_active=True)
        premium_offers = PremiumOffer.objects.filter(order_type='buy', share=share, is_active=True, price=share.current_price)
        seller_inventory = Inventory.objects.get(owner=instance.user)

        for buyer_offer in premium_offers:
            if buyer_offer.user != instance.user:
                buyer_inventory_share = InventoryShare.objects.get(owner=buyer_offer.user, share=share)
                buyer_inventory = Inventory.objects.get(owner=buyer_offer.user)

                creation_trade_using_offers(
                    buyer_inventory_share=buyer_inventory_share,
                    buyer_inventory=buyer_inventory,
                    seller_inventory=seller_inventory,
                    buyer_offer=buyer_offer,
                    seller_offer=instance,
                    global_inventory=global_inventory,
                    share=share
                )

        for buyer_offer in simple_offers:
            if buyer_offer.user != instance.user:
                buyer_inventory_share = InventoryShare.objects.get(owner=buyer_offer.user, share=share)
                buyer_inventory = Inventory.objects.get(owner=buyer_offer.user)

                creation_trade_using_offers(
                    buyer_inventory_share=buyer_inventory_share,
                    buyer_inventory=buyer_inventory,
                    seller_inventory=seller_inventory,
                    buyer_offer=buyer_offer,
                    seller_offer=instance,
                    global_inventory=global_inventory,
                    share=share
                )
        

    if instance.order_type == 'buy' and instance.is_active:
        simple_offers = SimpleOffer.objects.filter(order_type='sell', share=share, is_active=True)
        premium_offers = PremiumOffer.objects.filter(order_type='buy', share=share, is_active=True, price=share.current_price)
        buyer_inventory = Inventory.objects.get(owner=instance.user)

        for seller_offer in premium_offers:
            if seller_offer.user != instance.user:
                seller_inventory = Inventory.objects.get(owner=seller_offer.user)
                buyer_inventory_share = InventoryShare.objects.get(owner=instance.user, share=share)

                creation_trade_using_offers(
                    buyer_inventory_share=buyer_inventory_share,
                    buyer_inventory=buyer_inventory,
                    seller_inventory=seller_inventory,
                    buyer_offer=instance,
                    seller_offer=seller_offer,
                    global_inventory=global_inventory,
                    share=share
                )

        for seller_offer in simple_offers:
            if seller_offer.user != instance.user:
                seller_inventory = Inventory.objects.get(owner=seller_offer.user)

                creation_trade_using_offers(
                    buyer_inventory_share=InventoryShare.objects.get(owner=instance.user, share=share),
                    buyer_inventory=buyer_inventory,
                    seller_inventory=seller_inventory,
                    buyer_offer=instance,
                    seller_offer=seller_offer,
                    global_inventory=global_inventory,
                    share=share
                )


@transaction.atomic
@receiver(post_save, sender=PremiumOffer)
def trading_by_premium_offer(sender, instance, *args, **kwargs):
    share = instance.share
    global_inventory = GlobalInventory.objects.get(share=share)

    if instance.order_type == 'sell' and instance.is_active and instance.price == share.current_price:

        simple_offers = SimpleOffer.objects.filter(order_type='buy', share=share, is_active=True)
        premium_offers = PremiumOffer.objects.filter(order_type='buy', share=share, is_active=True, price=share.current_price)
        seller_inventory = Inventory.objects.get(owner=instance.user)

        for buyer_offer in premium_offers:
            if buyer_offer.user != instance.user:
                buyer_inventory_share = InventoryShare.objects.get(owner=buyer_offer.user, share=share)
                buyer_inventory = Inventory.objects.get(owner=buyer_offer.user)

                creation_trade_using_offers(
                    buyer_inventory_share=buyer_inventory_share,
                    buyer_inventory=buyer_inventory,
                    seller_inventory=seller_inventory,
                    buyer_offer=buyer_offer,
                    seller_offer=instance,
                    global_inventory=global_inventory,
                    share=share
                )


        for buyer_offer in simple_offers:
            if buyer_offer.user != instance.user:
                buyer_inventory_share = InventoryShare.objects.get(owner=buyer_offer.user, share=share)
                buyer_inventory = Inventory.objects.get(owner=buyer_offer.user)

                creation_trade_using_offers(
                    buyer_inventory_share=buyer_inventory_share,
                    buyer_inventory=buyer_inventory,
                    seller_inventory=seller_inventory,
                    buyer_offer=buyer_offer,
                    seller_offer=instance,
                    global_inventory=global_inventory,
                    share=share
                )
        

    if instance.order_type == 'buy' and instance.is_active and instance.price == share.current_price:
        simple_offers = SimpleOffer.objects.filter(order_type='sell', share=share, is_active=True)
        premium_offers = PremiumOffer.objects.filter(order_type='buy', share=share, is_active=True, price=share.current_price)
        buyer_inventory = Inventory.objects.get(owner=instance.user)

        for seller_offer in premium_offers:
            if seller_offer.user != instance.user:
                seller_inventory = Inventory.objects.get(owner=seller_offer.user)
                buyer_inventory_share = InventoryShare.objects.get(owner=instance.user, share=share)

                creation_trade_using_offers(
                    buyer_inventory_share=buyer_inventory_share,
                    buyer_inventory=buyer_inventory,
                    seller_inventory=seller_inventory,
                    buyer_offer=instance,
                    seller_offer=seller_offer,
                    global_inventory=global_inventory,
                    share=share
                )

        for seller_offer in simple_offers:
            if seller_offer.user != instance.user:
                seller_inventory = Inventory.objects.get(owner=seller_offer.user)

                creation_trade_using_offers(
                    buyer_inventory_share=InventoryShare.objects.get(owner=instance.user, share=share),
                    buyer_inventory=buyer_inventory,
                    seller_inventory=seller_inventory,
                    buyer_offer=instance,
                    seller_offer=seller_offer,
                    global_inventory=global_inventory,
                    share=share
                )