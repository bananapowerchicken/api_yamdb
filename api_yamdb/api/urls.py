from django.urls import path

from .views import register, get_user_token

urlpatterns = [
    
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_user_token, name='token')
   
]
