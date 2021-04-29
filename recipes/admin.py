from django.contrib import admin

from .models import Ingredient, Recipe, Tag, IngredientRecipe


class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    search_fields = ('title',)
    list_display = ("title", "dimension")
    list_filter = ("title",)


class IngredientRecipeAdmin(admin.ModelAdmin):
    model = IngredientRecipe


class IngredientRecipeInLine(admin.TabularInline):
    model = Recipe.ingredients.through
    extra = 1
    autocomplete_fields = ['ingredient', ]


class RecipeAdmin(admin.ModelAdmin):
    model = Recipe

    def favorites_count(self, obj):
        return obj.liked.count()

    favorites_count.short_description = "Favorites Count"

    inlines = (IngredientRecipeInLine,)
    # перечисляем поля, которые должны отображаться в админке
    list_display = ("title", "author", "favorites_count")
    # добавляем интерфейс для поиска по тексту постов
    search_fields = ("text",)
    # добавляем возможность фильтрации по дате
    list_filter = ("author", "title", "tags")


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag)
admin.site.register(IngredientRecipe, IngredientRecipeAdmin)
