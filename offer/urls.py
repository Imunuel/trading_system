from rest_framework.routers import DefaultRouter

from .views import ListAllOffer
router = DefaultRouter()

router.register(r'', ListAllOffer, basename='simple_offers')

user_patterns = [
] + router.urls

urlpatterns = user_patterns