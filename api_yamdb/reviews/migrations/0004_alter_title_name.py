# Generated by Django 3.2 on 2023-01-27 19:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reviews', '0003_auto_20230127_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='title',
            name='name',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(limit_value=256, message='Название произведения не может быть длиннее 256 символов.')]),
        ),
    ]
