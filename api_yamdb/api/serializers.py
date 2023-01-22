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
    #     # а эти строки просто работают корректно как валидатор
        if value.lower() == 'me':
            raise serializers.ValidationError("Username 'me' is not valid")
    #     # а вот эти строки по какой-то причине вызывают больше положеного ошибок - 5 вместо 8 пройденных тестов
        # как будто в этом условии загифрован запрет на me...
        # if not re.search(value, r'^[\w.@+-]+\z'):
        # if not re.search(r'^[\w.@+-]+\z', value):
        # if not re.fullmatch(r'^[\w.@+-]+\z', value):
        # if not re.match(r'^[\w.@+-]+\z', value): # либо просто некорректно использую условие - пока это самое здравое, что пришло мне в голову
        #     raise serializers.ValidationError('Username contains restricted symbols')
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
