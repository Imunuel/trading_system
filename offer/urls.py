from rest_framework.routers import DefaultRouter

from .views import ListAllOffer, UpdateDeleteMySimpleOfferAPI, UpdateDeleteMyPremiumOfferAPI
router = DefaultRouter()

router.register(r'', ListAllOffer, basename='simple_offers')
router.register(r'change/simple', UpdateDeleteMySimpleOfferAPI, basename='change_simple')
router.register(r'change/premium', UpdateDeleteMyPremiumOfferAPI, basename='change_premium')

user_patterns = [
] + router.urls

urlpatterns = user_patterns