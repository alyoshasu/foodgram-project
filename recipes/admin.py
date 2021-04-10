from django.contrib import admin

from .models import Ingredient, Recipe, Tag, Ingredient_quantity


admin.site.register(Ingredient)
admin.site.register(Recipe)
admin.site.register(Tag)
admin.site.register(Ingredient_quantity)
