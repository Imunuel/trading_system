from rest_framework.routers import DefaultRouter

from .views import (
    ShareListAPI
    )
router = DefaultRouter()

router.register(r'', ShareListAPI, basename='list_shares')


user_patterns = [
] + router.urls

urlpatterns = user_patterns