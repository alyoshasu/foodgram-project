from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from recipes.models import Recipe


def index(request):
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        "index.html",
        {'page': page, 'paginator': paginator, 'index': True, 'follow': False},
    )


def recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)

    return render(
        request,
        "recipes/recipe_view.html",
        {'recipe': recipe},
    )

