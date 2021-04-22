from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
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

    def perform_create(self, serializer):
        recipe_id = self.kwargs.get('id')
        print(recipe_id)
        print(self.request.user.username)
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(user=self.request.user, recipe=recipe)

