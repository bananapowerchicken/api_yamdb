from django.db import models


class Title(models.Model):
    name = models.CharField(
        max_length=256,
        verbose_name='Навзвание произведения'
    )
    year = models.SmallIntegerField(
        verbose_name='Год создания произведения'
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'

    def __str__(self):
        return self.name[:15]
