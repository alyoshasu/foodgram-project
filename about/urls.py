from django.urls import path
from . import views

urlpatterns = [
    path('author/', views.author, name='about_author'),
    path('technologies/', views.technologies, name='about_technologies'),
    path('project/', views.project, name='about_project'),
]
