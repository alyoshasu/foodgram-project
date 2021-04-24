from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, viewsets, filters, permissions
from recipes.models import Ingredient, Tag, Recipe, IngredientRecipe
from users.models import Follow, PurchaseQuantity, Favorite
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer, IngredientRecipeSerializer, \
    FollowSerializer, Purchase_quantitySerializer, FavoriteSerializer
User = get_user_model()


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', ]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'recipe_id'

    def perform_create(self, serializer):
        recipe_id = self.request.data['id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(recipe=recipe)


