from django.contrib import admin
from django.contrib.auth import get_user_model

from .models import Favorite, Purchase, Subscription

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_filter = ("email", "username")


admin.site.unregister(User)
admin.site.register(User, UserAdmin)
admin.site.register(Subscription)
admin.site.register(Purchase)
admin.site.register(Favorite)
