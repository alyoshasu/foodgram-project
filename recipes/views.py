from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from recipes.models import Recipe

from datetime import datetime

from .forms import RecipeForm

User = get_user_model()


def index(request):
    recipe_list = Recipe.objects.all()
    paginator = Paginator(recipe_list, 10)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        "index.html",
        {'page': page, 'paginator': paginator},
    )


def recipe(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    ingredients = recipe.ingredients_quantity.all()
    return render(
        request,
        "recipes/recipe_view.html",
        {
            'recipe': recipe,
            'ingredients': ingredients,
         },
    )


@login_required
def follow(request):
    follow_list = User.objects.filter(following__user=request.user)
    paginator = Paginator(follow_list, 10)  # показывать по 10 записей на странице.

    page_number = request.GET.get('page')  # переменная в URL с номером запрошенной страницы
    page = paginator.get_page(page_number)  # получить записи с нужным смещением

    return render(
        request,
        'authors/follow.html',
        {'page': page, 'paginator': paginator},
    )


@login_required
def recipe_new(request):
    if not request.method == 'POST':
        form = RecipeForm()
        return render(
            request,
            'recipes/recipe_new.html',
            {'form': form, 'is_edit': False},
        )

    form = RecipeForm(
        request.POST,
        files=request.FILES or None,
    )
    if not form.is_valid():
        return render(
            request,
            'recipes/recipe_new.html',
            {'form': form, 'is_edit': False}
        )

    recipe = form.save(commit=False)
    recipe.author = request.user
    recipe.pub_date = datetime.now()
    recipe.save()

    return redirect('index')


@login_required
def recipe_edit(request, slug):
    recipe = get_object_or_404(Recipe, slug=slug)
    if not recipe.author == request.user:
        return redirect('recipe', slug=slug)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=recipe,
    )
    if not request.method == 'POST':
        return render(
            request,
            'recipes/recipe_new.html',
            {'recipe': recipe,
             'form': form,
             'is_edit': True
             }
        )
    if not form.is_valid():
        return render(
            request,
            'recipes/recipe_new.html',
            {'recipe': recipe,
             'form': form,
             'is_edit': True
             }
        )
    form.save()
    return redirect('recipe', slug=form.cleaned_data.get("slug"))


def list_download(request):
    pass
