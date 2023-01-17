from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    class UserRole(models.TextChoices):
        USER = 'user',
        MODERATOR = 'moderator',
        ADMIN = 'admin'

    role = models.CharField(
        choices=UserRole.choices,
        default=UserRole.USER,
    )

    bio = models.TextField(
        'Биография',
        blank=True,
    )
