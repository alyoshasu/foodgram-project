from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('follow/', views.follow, name="follow"),
    path('favorites/', views.favorite, name="favorites"),
    path('purchase/', views.purchase, name="purchase"),
    path('purcase/download', views.list_download, name="purchase_list"),
    path('new/', views.recipe_new, name='recipe_new'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('recipe/<slug:slug>/', views.recipe, name='recipe'),
    path('recipe/<slug:slug>/edit/', views.recipe_edit, name='recipe_edit'),
    path('recipe/<slug:slug>/delete/', views.recipe_delete, name='recipe_delete'),
]
