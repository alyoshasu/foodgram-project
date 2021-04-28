from django.db import models

from django.contrib.auth import get_user_model

from recipes.models import Ingredient, Recipe

User = get_user_model()


class Subscription(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name="follower",
		verbose_name="Подписчик",
	)
	author = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name="following",
		verbose_name="Автор",
	)

	class Meta:
		unique_together = ['user', 'author']


class PurchaseList(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='purchases',
		verbose_name="Список покупок",
	)

	recipes = models.ManyToManyField(
		Recipe,
		verbose_name="Рецепты",
		related_name='in_purchase_list',
	)

	class Meta:
		pass


class Favorite(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='likes',
		verbose_name="Пользователь",
	)
	recipe = models.ForeignKey(
		Recipe,
		on_delete=models.CASCADE,
		related_name="liked",
		verbose_name="Рецепт",
	)

	class Meta:
		unique_together = ['user', 'recipe']
