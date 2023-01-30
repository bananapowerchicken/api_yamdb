from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User

admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'category',
        'name',
        'year'

    )
    search_fields = ('name',)
    list_filter = ('category',)
    empty_value_display = '-пусто-'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'slug'
    )
    search_fields = ('name',)
    list_filter = ('slug',)
    empty_value_display = '-пусто-'
