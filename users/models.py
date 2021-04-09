from django.db import models

from django.contrib.auth import get_user_model

from recipes.models import Ingredient

User = get_user_model()


class Follow(models.Model):
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


class Purchase_quantity(models.Model):
	user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='purchases',
		verbose_name="Список покупок",
	)
	ingredient = models.ForeignKey(
		Ingredient,
		on_delete=models.CASCADE,
		related_name='in_purchase',
	)
	quantity = models.IntegerField()

	class Meta:
		unique_together = ['user', 'ingredient']
