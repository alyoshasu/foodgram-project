from django.contrib import admin

from .models import Subscription, PurchaseQuantity, Favorite

admin.site.register(Subscription)
admin.site.register(PurchaseQuantity)
admin.site.register(Favorite)
