from django.urls import path

from .views import register

urlpatterns = [
    
    path('v1/auth/signup/', register, name='register'),
   
]
