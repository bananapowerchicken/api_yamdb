from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User

# admin.site.register(User)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('pk', 'username', 'email', 'role', 'first_name',
                    'last_name', 'bio')
