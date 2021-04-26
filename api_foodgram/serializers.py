from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.relations import PrimaryKeyRelatedField

from recipes.models import Ingredient, Tag, Recipe, IngredientRecipe
from users.models import Subscription, PurchaseQuantity, Favorite
User = get_user_model()


class IngredientSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Ingredient


class TagSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Tag


class RecipeSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Recipe


class IngredientRecipeSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = IngredientRecipe


class Purchase_quantitySerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = PurchaseQuantity


class FavoriteSerializer(serializers.ModelSerializer):
	recipe = serializers.SlugRelatedField(
		read_only=True,
		slug_field='title',
	)
	user = serializers.SlugRelatedField(
		queryset=User.objects.all(),
		default=serializers.CurrentUserDefault(),
		slug_field='username',
	)

	class Meta:
		fields = ['user', 'recipe']
		model = Favorite


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


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = User
