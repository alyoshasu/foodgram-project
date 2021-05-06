from django.urls import include, path
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter

from .views import (FavoritesViewSet, IngredientViewSet, PurchasesViewSet,
                    SubscriptionViewSet)

v1_router = DefaultRouter(trailing_slash=False)
v1_router.register(
    r'ingredients',
    IngredientViewSet,
    basename='IngredientView'
)
v1_router.register(
    r'subscriptions',
    SubscriptionViewSet,
    basename='SubscriptionView'
)
v1_router.register(r'favorites', FavoritesViewSet, basename='FavoritesView')
v1_router.register(r'purchases', PurchasesViewSet, basename='PurchasesView')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]

urlpatterns += [
    path('api-token-auth/', views.obtain_auth_token)
]
