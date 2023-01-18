from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):

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
    )
