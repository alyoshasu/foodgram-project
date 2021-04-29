from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Ingredient, Tag, Recipe, IngredientRecipe
from users.models import Subscription, Purchase, Favorite
User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Ingredient


class RecipeSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Recipe


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
		read_only=True,
		slug_field='username',
	)
	user = serializers.SlugRelatedField(
		queryset=User.objects.all(),
		default=serializers.CurrentUserDefault(),
		slug_field='username',
	)

	class Meta:
		fields = ['user', 'author']
		model = Subscription

