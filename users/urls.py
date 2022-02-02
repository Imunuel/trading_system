from rest_framework.routers import DefaultRouter

from .views import CreateUser, ChangeInventory
router = DefaultRouter()

router.register(r'create', CreateUser, basename='create_user')
router.register(r'inventory', ChangeInventory, basename='inventory')

user_patterns = [
] + router.urls

urlpatterns = user_patterns