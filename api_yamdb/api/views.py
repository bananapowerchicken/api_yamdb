from rest_framework import viewsets, permissions, status, mixins
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework_simplejwt.tokens import AccessToken

from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer, TitleSerializer,
                          UserSerializer, RegisterDataSerializer, TokenSerializer,
                          UserEditSerializer, AdminRegisterDataSerializer)
from reviews.models import User, Category, Comment, Genre, Review, Title
from .permissions import IsAdmin
from http import HTTPStatus
from .utils import send_confirmation_code
from rest_framework import filters




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
def register_by_admin(request):
    serializer = AdminRegisterDataSerializer(data=request.data)

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

    return Response(serializer.data, status=HTTPStatus.CREATED)


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


# class BaseUserViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.DestroyModelMixin,
#                         viewsets.GenericViewSet): 
#     pass  


# # class UserViewSet(BaseUserViewSet):
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes=[permissions.AllowAny]
    # http_method_names = ['get']
#     # lookup_field = 'username'
    # permission_classes = (IsAdmin, permissions.IsAuthenticated, )  # этот пермишн дает ошибку 405   
    
# #     @action(detail=False, methods=["get"])
# #     def get_users(self, request):
# #         if not request.user.is_authenticated:
# #             return Response(status=HTTPStatus.UNAUTHORIZED)
# #         return Response(status=HTTPStatus.FORBIDDEN)


    @action(
        methods=[
            "get",
            "patch",
        ],
        detail=False,
        url_path="me",
        permission_classes=[permissions.IsAuthenticated],         
    )
    def users_own_profile(self, request):
        user = request.user
        if request.method == "GET":

            # if not request.user.is_admin or request.user.is_superuser:
            #     return Response(HTTPStatus.FORBIDDEN)

            serializer = self.get_serializer(user)
            return Response(serializer.data, status=HTTPStatus.OK)
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

# class UserViewSet(viewsets.ModelViewSet):
#     http_method_names = ['get', 'post', 'patch', 'delete']
#     lookup_field = 'username'
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#     permission_classes = (IsAdmin,)
#     filter_backends = (filters.SearchFilter,)
#     search_fields = ('username',)

#     def list(self, request):
#         if not request.user.is_authenticated:
#             return Response(HTTPStatus.FORBIDDEN)
#         return Response(HTTPStatus.OK)

#     @action(
#     methods=['GET', 'PATCH'],
#     detail=False,
#     url_path='me',
#     permission_classes=[permissions.IsAuthenticated]
#     )
#     def me_page(self, request):  # то есть тут я так понимаю любым мб название ф-ии
#         if request.method == 'GET':
#             serializer = UserSerializer(request.user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         if request.method == 'PATCH':
#             serializer = UserSerializer(
#             request.user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save(role=request.user.role)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors,
#         status=status.HTTP_400_BAD_REQUEST)


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

