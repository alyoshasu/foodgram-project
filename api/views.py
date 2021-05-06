from django.contrib.auth import get_user_model
from rest_framework import filters, status, viewsets, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from recipes.models import Ingredient, Recipe

from .permissions import IsAdminOrReadOnlyPermission
from .serializers import (FavoriteSerializer, IngredientSerializer,
                          PurchaseSerializer, SubscriptionSerializer)

User = get_user_model()


class DestroyModelMixin:
    def destroy(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        if self.kwargs.get('author'):
            author = get_object_or_404(
                User,
                username=self.kwargs.get('author')
            )
            instance = get_object_or_404(
                queryset,
                author=author,
                user=self.request.user
            )
        elif self.kwargs.get('recipe'):
            recipe = get_object_or_404(Recipe, title=self.kwargs.get('recipe'))

            instance = get_object_or_404(
                queryset,
                recipe=recipe,
                user=self.request.user
            )

        self.perform_destroy(instance)
        return Response({"deleted": "ok"}, status=status.HTTP_200_OK)

    def perform_destroy(self, instance):
        instance.delete()


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes = (IsAdminOrReadOnlyPermission,)
    search_fields = ['title', ]


class SubscriptionViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    serializer_class = SubscriptionSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'author'

    def get_queryset(self):
        owner_queryset = self.request.user.follower.all()
        return owner_queryset


class FavoritesViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    serializer_class = FavoriteSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'recipe'

    def get_queryset(self):
        owner_queryset = self.request.user.likes.all()
        return owner_queryset


class PurchasesViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet
):
    serializer_class = PurchaseSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'recipe'

    def get_queryset(self):
        owner_queryset = self.request.user.purchases.all()
        return owner_queryset
