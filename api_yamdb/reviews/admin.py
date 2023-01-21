from django.contrib import admin

from .models import Review, User

admin.site.register(User)
admin.site.register(Review)
