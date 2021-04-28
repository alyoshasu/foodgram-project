from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework import generics, viewsets, filters, permissions
from recipes.models import Ingredient, Tag, Recipe, IngredientRecipe
from users.models import Subscription, Purchase, Favorite
from .serializers import IngredientSerializer, TagSerializer, RecipeSerializer, IngredientRecipeSerializer, \
    SubscriptionSerializer, Purchase_quantitySerializer, FavoriteSerializer, PurchaseSerializer

User = get_user_model()


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', ]


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'author_id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"deleted": "ok"}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        author_id = self.request.data['id']
        author = get_object_or_404(User, id=author_id)
        serializer.save(author=author)


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'recipe_id'

    def perform_create(self, serializer):
        recipe_id = self.request.data['id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(recipe=recipe)


class PurchasesViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'recipe_id'

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"deleted": "ok"}, status=status.HTTP_200_OK)

    def perform_create(self, serializer):
        recipe_id = self.request.data['id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        serializer.save(recipe=recipe)
