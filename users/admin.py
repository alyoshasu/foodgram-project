from django.contrib import admin

from .models import Follow, Purchase_quantity, Favorite

admin.site.register(Follow)
admin.site.register(Purchase_quantity)
admin.site.register(Favorite)
