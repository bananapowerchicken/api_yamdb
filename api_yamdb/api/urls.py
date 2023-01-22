from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import register, get_user_token, UserViewSet


router = DefaultRouter()
router.register('users', UserViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_user_token, name='token')
]
