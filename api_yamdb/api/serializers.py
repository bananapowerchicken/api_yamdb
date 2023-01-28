from django.core.validators import MaxLengthValidator, RegexValidator
from django.db.models import Sum
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, Review, Title, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email', 'first_name', 'last_name', 'bio',
                  'role')
        model = User


class RegisterDataSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError("Username 'me' is not valid")
        return value

    class Meta:
        fields = ('username', 'email')
        model = User


class AdminRegisterDataSerializer(serializers.ModelSerializer):
    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError("Username 'me' is not valid")
        return value

    class Meta:
        fields = ('username', 'email',  'first_name', 'last_name')
        model = User


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()


class UserEditSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("username", "email", "first_name",
                  "last_name", "bio", "role")
        model = User
        read_only_fields = ('role',)


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для работы с категориями."""

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с жанрами произведений."""

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(), slug_field='slug', many=True
    )

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'category',
            'genre',
        )


class TitleSerializerRead(serializers.ModelSerializer):
    """Сериализатор для работы с произведениями при чтении."""
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(many=True, read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = (
            'id', 'name', 'description', 'year', 'category', 'genre', 'rating'
        )
        read_only_fields = ('id',)

    def get_rating(self, obj):
        score_sum = Review.objects.filter(title_id=obj.id).aggregate(
            Sum('score')).get('score__sum')
        score_sum = int(0 if score_sum is None else score_sum)
        score_count = Review.objects.filter(title_id=obj.id).count()
        if score_count == 0:
            return None
        rating = score_sum / score_count
        rating = int(rating + (0.5 if rating > 0 else -0.5))
        return round(rating)


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        author = self.context.get('request').user
        if (title.reviews.filter(author=author).exists() and self.context.get('request').method != 'PATCH'):
            raise serializers.ValidationError(
                'Вы можете оставить только один отзыв на произведение.'
            )
        return data


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username')

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')
