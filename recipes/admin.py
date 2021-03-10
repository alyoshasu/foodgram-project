from django.contrib import admin

from .models import Ingredient, Recipe, Tag, Total_ingredients

admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Total_ingredients)
