from rest_framework import serializers

from reviews.models import Title


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
