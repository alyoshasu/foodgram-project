from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets, filters
from recipes.models import Ingredient, Recipe
from users.models import Subscription, Purchase, Favorite
from .permissions import IsAdminOrReadOnlyPermission
from .serializers import IngredientSerializer, SubscriptionSerializer, FavoriteSerializer, PurchaseSerializer

User = get_user_model()


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = (IsAdminOrReadOnlyPermission,)
    search_fields = ['title', ]


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'author'

    def get_queryset(self):
        owner_queryset = self.queryset.filter(user=self.request.user)
        return owner_queryset

    def destroy(self, request, *args, **kwargs):
        username = self.kwargs.get('author')
        author = get_object_or_404(User, username=username)
        instance = get_object_or_404(Subscription, author=author, user=self.request.user)
        self.perform_destroy(instance)
        return Response({"deleted": "ok"}, status=status.HTTP_200_OK)


class FavoritesViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'recipe'

    def get_queryset(self):
        owner_queryset = self.queryset.filter(user=self.request.user)
        return owner_queryset

    def destroy(self, request, *args, **kwargs):
        recipe_title = self.kwargs.get('recipe')
        recipe = get_object_or_404(Recipe, title=recipe_title)
        instance = get_object_or_404(Favorite, recipe=recipe, user=self.request.user)
        self.perform_destroy(instance)
        return Response({"deleted": "ok"}, status=status.HTTP_204_NO_CONTENT)


class PurchasesViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'recipe'

    def get_queryset(self):
        owner_queryset = self.queryset.filter(user=self.request.user)
        return owner_queryset

    def destroy(self, request, *args, **kwargs):
        recipe_title = self.kwargs.get('recipe')
        recipe = get_object_or_404(Recipe, title=recipe_title)
        instance = get_object_or_404(Purchase, recipe=recipe, user=self.request.user)
        self.perform_destroy(instance)
        return Response({"deleted": "ok"}, status=status.HTTP_204_NO_CONTENT)
