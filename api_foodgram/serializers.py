from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Ingredient, Recipe
from users.models import Subscription, Purchase, Favorite
User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Ingredient


class FavoriteSerializer(serializers.ModelSerializer):
	recipe = serializers.SlugRelatedField(
		queryset=Recipe.objects.all(),
		slug_field='title',
	)
	user = serializers.HiddenField(
		default=serializers.CurrentUserDefault(),
	)

	class Meta:
		fields = ['user', 'recipe']
		model = Favorite


class PurchaseSerializer(serializers.ModelSerializer):
	recipe = serializers.SlugRelatedField(
		queryset=Recipe.objects.all(),
		slug_field='title',
	)
	user = serializers.HiddenField(
		default=serializers.CurrentUserDefault(),
	)

	class Meta:
		fields = ['user', 'recipe']
		model = Purchase


class SubscriptionSerializer(serializers.ModelSerializer):
	author = serializers.SlugRelatedField(
		queryset=User.objects.all(),
		slug_field='username',
	)
	user = serializers.HiddenField(
		default=serializers.CurrentUserDefault(),
	)

	class Meta:
		fields = ['user', 'author']
		model = Subscription

