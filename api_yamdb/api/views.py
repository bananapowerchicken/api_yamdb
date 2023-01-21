from rest_framework import viewsets

from reviews.models import User, Title, Category, Genre

from .serializers import (
    UserSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializer
    lookup_field = 'name'


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    search_fields = ['name']
    lookup_field = 'slug'
