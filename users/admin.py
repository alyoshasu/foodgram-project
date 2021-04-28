from django.contrib import admin

from .models import Subscription, PurchaseList, Favorite

admin.site.register(Subscription)
admin.site.register(PurchaseList)
admin.site.register(Favorite)
