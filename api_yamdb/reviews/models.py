from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class User(AbstractUser):

    USER_ROLE_CHOICES = [
        ('USR', 'user'),
        ('MOD', 'moderator'),
        ('ADM', 'admin'),
    ]

    role = models.CharField(
        max_length=3,
        choices=USER_ROLE_CHOICES,
        default='USR',
    )

    bio = models.TextField(
        'Биография',
        blank=True,
        null=True,
    )

    email = models.EmailField(
        'Адрес электронной почты',
        unique=True,
        max_length=254,
    )

    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
        null=True,
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        null=True,
    )

    REQUIRED_FIELDS = ['email']

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='username_is_not_me',
            )
        ]


class Review(models.Model):
    """Модель отзыва."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    text = models.TextField(
        'Текст отзыва'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
        related_name='reviews'
    )
    score = models.IntegerField(
        'Оценка',
        help_text='Оцените произведение от 1 до 10',
        validators=[
            MinValueValidator(1, message='Минимальная оценка - 1'),
            MaxValueValidator(10, message='Максимальная оценка - 10')
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления отзыва',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text
