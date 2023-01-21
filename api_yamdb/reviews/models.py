from django.contrib.auth.models import AbstractUser
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
        null=True,
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


class Category(models.Model):
    name = models.CharField(
        max_length=256,
        default='--Пусто--',
        verbose_name='Название категории'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Конвертер пути'
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:15]


class Genre(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название жанра'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='Конвертер пути'
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
        blank=False
    )
    year = models.SmallIntegerField(
        verbose_name='Год создания произведения'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        db_index=True,
        blank=False,
        verbose_name='Жанр произведения'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name='titles',
        verbose_name='Категория'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'year'],
                name='unique_name_year'
            )
        ]

    def __str__(self):
        return self.name[:15]
