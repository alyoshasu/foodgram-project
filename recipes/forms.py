from django import forms
from django.forms import inlineformset_factory

from .models import Recipe, Ingredient, IngredientRecipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = [
            'title',
            'image',
            'description',
            # 'ingredients',
            'tags',
            'time',
            'slug',
        ]

    help_texts = {
        'title': 'Введите название вашего рецепта',
        'image': 'Добавьте изображение',
        'description': 'Введите описание вашего рецепта',
        'ingredients': 'Список ингредиентов',
        'tags': 'Теги',
        'time': 'Время приготовления',
        'slug:': 'описание для ссылки',
    }


RecipeFormSet = inlineformset_factory(Recipe, Recipe.ingredients.through, fields=['ingredient', 'quantity'], extra=1)
# RecipeFormSet = inlineformset_factory(Ingredient, Recipe, fields=['recipe', 'ingredient', 'quantity'])
