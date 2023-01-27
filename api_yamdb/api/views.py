from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from http import HTTPStatus
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Genre, Review, Title, User

from .filters import TitleFilterSet
from .permissions import IsAdmin, IsAdminOrReadOnly, IsAdminOrAuthorOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegisterDataSerializer,
                          ReviewSerializer, TitleSerializer,
                          TitleSerializerCreate, TitleSerializerRead,
                          TokenSerializer, UserEditSerializer, UserSerializer)
from .utils import send_confirmation_code
from .mixins import ListCreateDestroyViewSet


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterDataSerializer(data=request.data)

    email=request.data.get('email')
    username=request.data.get('username')

    if User.objects.filter(username=username, email=email).exists():
        user = User.objects.get(username=username, email=email)
        send_confirmation_code(user)

        return Response(status=HTTPStatus.OK)

    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username'],
    )
    send_confirmation_code(user)

    return Response(serializer.data, status=HTTPStatus.OK)

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_user_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    if default_token_generator.check_token(
        user,
        serializer.validated_data['confirmation_code']
    ):
        token = AccessToken.for_user(user)
        return Response({"token": str(token)}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ('get', 'patch', 'delete', 'post')
    queryset = User.objects.all()
    serializer_class = UserSerializer 
    lookup_field = 'username'
    permission_classes = ( IsAdmin , )
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)

    @action(
        methods=['get', 'patch'],
        detail=False,
        url_path='me',
        permission_classes=[permissions.IsAuthenticated],    
        serializer_class=UserEditSerializer,     
        pagination_class = PageNumberPagination
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=HTTPStatus.OK)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class TitleViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с произведениями."""
    queryset = Title.objects.all().order_by('name')
    serializer_class = TitleSerializer
    permission_classes = (IsAdminOrReadOnly,)
    lookup_field = 'name'
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializerRead


class CategoryViewSet(ListCreateDestroyViewSet):
    """ViewSet для работы с категориями."""
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(ListCreateDestroyViewSet):
    """ViewSet для работы с жанрами."""
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для просмотра и редактирования отзывов."""
    serializer_class = ReviewSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrAuthorOrReadOnly
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """ViewSet для просмотра и редактирования комментариев к отзывам."""
    serializer_class = CommentSerializer
    permission_classes = [
        permissions.IsAuthenticatedOrReadOnly,
        IsAdminOrAuthorOrReadOnly
    ]

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title_id=title_id, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
<<<<<<< HEAD
        review = get_object_or_404(Review, title_id=title_id, id=review_id)
        serializer.save(author=self.request.user, review=review)
=======
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, title=title, review=review)
>>>>>>> fix-tests-title
