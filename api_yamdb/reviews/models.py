from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


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
        # username__regex=r'^[\w.@+-]+\z'
        # validators=[
        #     RegexValidator(
        #         regex=r'^[\w.@+-]+\z',
        #         message='Username contains restricted symbols',
        #     ),
        # ]
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

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=~models.Q(username='me'),
                name='username_is_not_me',
            ),
            # models.CheckConstraint(
            #     check=models.Q(username__regex=r'^[\w.@+-]+\z'),
            #     name='username_contains_restricted_symbols',
            # )        
            
        ]
