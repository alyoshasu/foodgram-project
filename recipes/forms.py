from django import forms
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

	help_texts = {
		'title': 'Введите название вашего рецепта',
		'image': 'Добавьте изображение',
		'description': 'Введите описание вашего рецепта',
		'ingredients': 'Список ингредиентов',
		'tags': 'Теги',
		'time': 'Время приготовления',
		'slug:': 'описание для ссылки',
	}
