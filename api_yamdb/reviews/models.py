from django.contrib.auth.models import AbstractUser
from django.core.validators import (MaxLengthValidator, MaxValueValidator,
                                    MinValueValidator, RegexValidator)
from django.db import models
from django.utils.translation import gettext_lazy as _

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
        _('Название категории'),
        max_length=256,
        default='--Пусто--',
    )
    slug = models.SlugField(
        _('Конвертер пути'),
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name[:15]


class Genre(models.Model):
    """Модель для работы с жанрами"""
    name = models.CharField(
        _('Название жанра'),
        max_length=256,
    )
    slug = models.SlugField(
        _('Конвертер пути'),
        max_length=50,
        unique=True,
    )

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'

    def __str__(self):
        return self.name[:15]


class Title(models.Model):
    """Модель для работы с произведениями"""
    name = models.CharField(
        _('Название произведения'),
        max_length=256, blank=False,
        validators=[
            MaxLengthValidator(
                limit_value=256,
                message='Не более 256 символов.')
        ]
    )
    year = models.PositiveSmallIntegerField(
        _('Год создания произведения'),
        validators=[year_validator],
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )
    genre = models.ManyToManyField(
        Genre,
        through='GenreToTitle',
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


class GenreToTitle(models.Model):
    """Модель связывающая произведение с жанром"""
    title = models.ForeignKey(
        Title,
        on_delete=models.CASCADE,
        related_name='genretitles',
    )
    genre = models.ForeignKey(
        Genre,
        on_delete=models.SET_NULL,
        null=True,
        related_name='genretitles',
    )

    class Meta:
        ordering = ('genre',)

    def __str__(self):
        return f'{self.title} {self.genre}'


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
        ordering = ['title']
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

    class Meta:
        ordering = ['pub_date']