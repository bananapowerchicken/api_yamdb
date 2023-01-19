from rest_framework import serializers

from reviews.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = CustomUser
