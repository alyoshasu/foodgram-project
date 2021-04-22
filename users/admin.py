from django.contrib import admin

from .models import Follow, PurchaseQuantity, Favorite

admin.site.register(Follow)
admin.site.register(PurchaseQuantity)
admin.site.register(Favorite)
