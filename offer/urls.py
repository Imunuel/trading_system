from rest_framework.routers import DefaultRouter

from .views import (
    ListAllOffer, 
    ActivateAllOfferAPI, 
    ChangeMySimpleOffersAPI, 
    ChangeMyPremiumOffersAPI,
    DeleteSimpleOfferAPI,
    DeletePremiumOfferAPI,
    TradeAPI
    )
router = DefaultRouter()

router.register(r'', ListAllOffer, basename='simple_offers')
router.register(r'change/simple', ChangeMySimpleOffersAPI, basename='change_simple')
router.register(r'change/premium', ChangeMyPremiumOffersAPI, basename='change_premium')
router.register(r'delete/simple', DeleteSimpleOfferAPI, basename='delete_simple')
router.register(r'delete/premium', DeletePremiumOfferAPI, basename='delete_premium')
router.register(r'', ActivateAllOfferAPI, basename='activate_all')
router.register(r'trades', TradeAPI, basename='trade')


user_patterns = [
] + router.urls

urlpatterns = user_patterns