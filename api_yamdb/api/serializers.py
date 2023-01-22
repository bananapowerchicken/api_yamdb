from rest_framework import serializers
# from rest_framework.validators import RegexValidator
from django.core.validators import RegexValidator

from reviews.models import User
import re


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(
    #     validators=[
    #             RegexValidator(
    #                 regex=r'^[\w.@+-]+\z',
    #                 message='Username contains restricted symbols',
    #                 code='invalid_username'
    #             ),
    #         ]
    # )

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = User


class RegisterDataSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError("Username 'me' is not valid")
        if not re.search(value, r'^[\w.@+-]+\z'):
            raise serializers.ValidationError('Username contains restricted symbols')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
