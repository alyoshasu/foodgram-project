from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('follow/', views.follow, name="follow"),
    path('new/', views.recipe_new, name='recipe_new'),
    path('<slug:slug>/', views.recipe, name='recipe'),
    path('<slug:slug>/edit/', views.recipe_edit, name='recipe_edit'),
]
