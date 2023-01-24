from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from reviews.models import Category, Comment, Genre, Review, Title, User

from .filters import TitleFilterSet
from .permissions import IsAdmin, TitlePermission
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegisterDataSerializer,
                          ReviewSerializer, TitleSerializer,
                          TitleSerializerCreate, TitleSerializerRead,
                          TokenSerializer, UserEditSerializer, UserSerializer)

yamdb_mail = 'YaMDb@gmail.com'

# регистрация по api для любого желающего
@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data['username']
    )
    # создаю токен и сразу привязываю его к объекту user
    confirmation_code = default_token_generator.make_token(user)
    # и теперь надо этот код отправить по почте
    send_mail(
        'YaMDb registration',
        f'Here is your confirmation code to use: {confirmation_code}',
        yamdb_mail,  # мб тут просто None поставить и это вообще не нужно?
        [user.email],
        fail_silently=False,
    )

    # не знаю, что тут грамотнее возвращать, пока оставлю такой вариант
    return Response(serializer.data, status=status.HTTP_200_OK)


# получение токена после регистрации для любого желающего по API
@api_view(["POST"])
@permission_classes([permissions.AllowAny])  # но мб тут дб только авторизованные - не знаю
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
    http_method_names = ['post', 'get', 'patch', 'delete']  # эта строка будто тоже не имеет влияния!
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)

    @action(
        methods=[
            "get",
            "patch",
        ],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],
        serializer_class=UserEditSerializer,
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == "GET":
            serializer = self.get_serializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        if request.method == "PATCH":
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
    permission_classes = (TitlePermission,)
    lookup_field = 'name'
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilterSet

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH', 'DELETE',):
            return TitleSerializerCreate
        return TitleSerializerRead


class CategoryViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с категориями."""
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer
    permission_classes = (TitlePermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    """ViewSet для работы с жанрами."""
    queryset = Genre.objects.all().order_by('name')
    serializer_class = GenreSerializer
    permission_classes = (TitlePermission,)
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """ViewSet для просмотра и редактирования отзывов."""
    serializer_class = ReviewSerializer

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

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, title_id=title_id, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(author=self.request.user, title=title, review=review)
