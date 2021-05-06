from django import forms
from django.forms import inlineformset_factory

from .models import Recipe


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
        # widgets = {'tags': forms.CheckboxSelectMultiple()}

    help_texts = {
        'title': 'Введите название вашего рецепта',
        'image': 'Добавьте изображение',
        'description': 'Введите описание вашего рецепта',
        # 'ingredients': 'Список ингредиентов',
        'tags': 'Теги',
        'time': 'Время приготовления',
        'slug:': 'описание для ссылки',
    }


RecipeFormSet = inlineformset_factory(
    Recipe, Recipe.ingredients.through,
    fields=['ingredient', 'quantity'],
    extra=1,
    help_texts={
        'ingredients': 'Список ингредиентов',
        'quantity': 'Введите кол-во',
    }
)
