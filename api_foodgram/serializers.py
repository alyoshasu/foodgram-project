from django.contrib.auth import get_user_model
from rest_framework import serializers

from recipes.models import Ingredient, Tag, Recipe, Total_ingredients
from users.models import Follow

User = get_user_model()


class RecipeSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Recipe


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = User


class IngredientSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Ingredient


class FollowSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Follow


class TagSerializer(serializers.ModelSerializer):
	class Meta:
		fields = '__all__'
		model = Tag
