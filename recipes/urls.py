from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('follow/', views.follow, name="follow"),
    path('new/', views.recipe_new, name='recipe_new'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('recipe/<slug:slug>/', views.recipe, name='recipe'),
    path('recipe/<slug:slug>/edit/', views.recipe_edit, name='recipe_edit'),
]
