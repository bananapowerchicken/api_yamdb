# Generated by Django 3.2 on 2023-01-30 12:31

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0002_auto_20230128_1301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='score',
            field=models.PositiveSmallIntegerField(help_text='Оцените произведение от 1 до 10', validators=[django.core.validators.MinValueValidator(1, message='Минимальная оценка - 1'), django.core.validators.MaxValueValidator(10, message='Максимальная оценка - 10')], verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='title',
            name='genre',
            field=models.ManyToManyField(db_index=True, to='reviews.Genre', verbose_name='Жанр произведения'),
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=150, unique=True, validators=[django.core.validators.RegexValidator('^[\\w-]+$', 'В username некорректные символы')], verbose_name='Имя пользователя'),
        ),
    ]