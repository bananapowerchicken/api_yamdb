from rest_framework import viewsets

from reviews.models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.permissions import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
   
