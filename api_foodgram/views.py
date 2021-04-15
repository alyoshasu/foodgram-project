from django.contrib.auth import get_user_model
from rest_framework import generics, viewsets, filters
from recipes.models import Ingredient, Tag, Recipe, IngredientRecipe
from users.models import Follow, Purchase_quantity, Favorite
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer, IngredientRecipeSerializer, FollowSerializer, Purchase_quantitySerializer, FavoriteSerializer
User = get_user_model()


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', ]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
