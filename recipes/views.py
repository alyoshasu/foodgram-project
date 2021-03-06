from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from recipes.models import Recipe


# def index(request):
#     latest_recipe_list = Recipe.objects.order_by('-pub_date')[:5]
#     output = ', '.join([r.title for r in latest_recipe_list])
#     return HttpResponse(output)


def index(request):
    latest_recipe_list = Recipe.objects.order_by('-pub_date')[:5]
    context = {'latest_recipe_list': latest_recipe_list}
    return render(request, "recipes/indexNotAuth.html", context)


def recipe(request, slug):
    return HttpResponse("You're looking at recipe '%s'." % get_object_or_404(
        Recipe,
        slug=slug,
    ).title
                        )
