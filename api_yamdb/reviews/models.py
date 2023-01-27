from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxValueValidator, MinValueValidator, 
                                    RegexValidator)
from django.db import models

from .validators import year_validator


class User(AbstractUser):
    
    ADMIN = 'admin'
    MODERATOR = 'moderator'
    USER = 'user'

    USER_ROLE_CHOICES = [
        (ADMIN, 'Administrator'),
        (MODERATOR, 'Moderator'),
        (USER, 'User'),
    ]
   
    role = models.CharField(
        max_length=150,
        choices=USER_ROLE_CHOICES,
        default=USER,
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
            RegexValidator(r'^[\w-]+$', "username содержит некорректные символы"),
        ],
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

    @property
    def is_admin(self):
        return self.role == self.ADMIN     
    
    class Meta:
        ordering = ['id']
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'


class Category(models.Model):
    """Модель для работы с категориями"""
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
    """Модель для работы с жанрами"""
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
    """Модель для работы с произведениями"""
    name = models.CharField(
        max_length=256,
        verbose_name='Название произведения',
        blank=False
    )
    year = models.SmallIntegerField(
        validators=[year_validator],
        verbose_name='Год создания произведения'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
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
            MinValueValidator(1),
            MaxValueValidator(10)
        ]
    )
    pub_date = models.DateTimeField(
        'Дата добавления отзыва',
        auto_now_add=True,
        db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name='unique_review',
                fields=['author', 'title'],
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    """Модель комментария к отзыву."""
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    review = models.ForeignKey(
        Review,
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    text = models.TextField(
        'Текст комментария'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор комментария',
        on_delete=models.CASCADE,
        related_name='comments'
    )
    pub_date = models.DateTimeField(
        'Дата добавления комментария',
        auto_now_add=True,
        db_index=True
    )

    def __str__(self):
        return self.text
