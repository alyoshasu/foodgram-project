from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Ingredient, Tag, Recipe, IngredientRecipe
from users.models import Follow, Purchase_quantity, Favorite
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


class FollowSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Follow


class Purchase_quantitySerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Purchase_quantity


class FavoriteSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Favorite


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = User
