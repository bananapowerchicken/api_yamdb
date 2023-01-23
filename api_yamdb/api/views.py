from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import AccessToken

from reviews.models import User
from .serializers import UserSerializer, RegisterDataSerializer, TokenSerializer, UserEditSerializer
from .permissions import IsAdmin


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


# получение токена после регистрации для люого желающего по API
@api_view(["POST"])
@permission_classes([permissions.AllowAny])  # но мб тут дб только авторизованные - не знаю
def get_user_token(request):
    # мне тут необх извлечь токен из юзера
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    # serializer.save()  # что делает эта штука?
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
    http_method_names = ['get', 'patch', 'delete']
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (IsAdmin,)

    # @action(
    #     methods=[
    #         "get",
    #         "patch",
    #     ],
    #     detail=False,
    #     url_path="me",
    #     permission_classes=[permissions.IsAuthenticated],
    #     serializer_class=UserEditSerializer,
    # )
    # def users_own_profile(self, request):
    #     user = request.user
    #     if request.method == "GET":
    #         serializer = self.get_serializer(user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     if request.method == "PATCH":
    #         serializer = self.get_serializer(
    #             user,
    #             data=request.data,
    #             partial=True
    #         )
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
