from rest_framework.routers import DefaultRouter

from .views import CreateUser
router = DefaultRouter()

router.register(r'create', CreateUser, basename='create_user')

user_patterns = [
] + router.urls

urlpatterns = user_patterns