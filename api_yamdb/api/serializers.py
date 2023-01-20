from rest_framework import serializers

from reviews.models import CustomUser, Title


class CustomUserSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = CustomUser
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )


class TitleSerializer(serializers.ModelSerializer):
    pass

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description'
        )
