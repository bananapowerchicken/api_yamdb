from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('pk', 'title_id', 'text', 'author', 'score', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('pk', 'review_id', 'text', 'author', 'pub_date')
    search_fields = ('text',)
    list_filter = ('pub_date',)
    empty_value_display = '-пусто-'
