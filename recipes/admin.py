from django.contrib import admin

from .models import Ingredient, Recipe, Tag, IngredientRecipe


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    search_fields = ['title', ]


class IngredientRecipeAdmin(admin.ModelAdmin):
    model = IngredientRecipe


class IngredientRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    autocomplete_fields = ['ingredient', ]


class RecipeAdmin(admin.ModelAdmin):
    inlines = (IngredientRecipeInLine, )


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
