from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (IngredientViewSet, RecipeViewSet, FollowViewSet, FavoritesViewSet)

from rest_framework.authtoken import views

v1_router = DefaultRouter()
v1_router.register(r'ingredients', IngredientViewSet, basename='IngredientView')
v1_router.register(r'recipes', RecipeViewSet, basename='RecipeView')
v1_router.register(r'follow', FollowViewSet, basename='FollowView')
v1_router.register(r'favorites', FavoritesViewSet, basename='FavoritesView')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
