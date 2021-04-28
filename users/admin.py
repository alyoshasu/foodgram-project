from django.contrib import admin

from .models import Subscription, Purchase, Favorite

admin.site.register(Subscription)
admin.site.register(Purchase)
admin.site.register(Favorite)
