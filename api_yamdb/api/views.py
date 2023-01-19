from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail

from reviews.models import CustomUser
from .serializers import CustomUserSerializer, RegisterDataSerializer


yamdb_mail = 'YaMDb@gmail.com'

@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterDataSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        CustomUser,
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

    return Response(status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    lookup_field = 'username'
