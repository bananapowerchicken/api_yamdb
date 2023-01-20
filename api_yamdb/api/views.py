from rest_framework import viewsets

from reviews.models import CustomUser, Title

from .serializers import CustomUserSerializer, TitleSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    lookup_field = 'name'
