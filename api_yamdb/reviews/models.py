from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator, MaxLengthValidator


class User(AbstractUser):

    USER_ROLE_CHOICES = (
        ('USR', 'user'),
        ('MOD', 'moderator'),
        ('ADM', 'admin'),
    )

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
        validators=[
            RegexValidator(r'^[\w.@+-]'),
            # MaxLengthValidator(150),  # вот этот валидатор- уже на регистрацию через admin не повлиял
        ],
    )

    first_name = models.CharField(
        'Имя',
        max_length=150,
        null=True,
        default=" "
    )

    last_name = models.CharField(
        'Фамилия',
        max_length=150,
        null=True,
    )

    REQUIRED_FIELDS = ['email']

    @property
    def is_admin(self):
        return self.role == 'ADM'
