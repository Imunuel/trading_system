from rest_framework.routers import DefaultRouter

from .views import CreateUser, ChangeInventory, FullInventoryAPI
router = DefaultRouter()

router.register(r'create', CreateUser, basename='create_user')
router.register(r'inventory', ChangeInventory, basename='inventory')
router.register(r'inventory', FullInventoryAPI, basename='full_inventory_user')

user_patterns = [
] + router.urls

urlpatterns = user_patterns