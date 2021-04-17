from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect

from recipes.models import Recipe, IngredientRecipe, Tag

from datetime import datetime

from .forms import RecipeForm, RecipeFormSet

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
    ingredients = IngredientRecipe.objects.filter(recipe=recipe)
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
    paginator = Paginator(follow_list, 10)

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'authors/follow.html',
        {'page': page, 'paginator': paginator},
    )


@login_required
def recipe_new(request):
    if not request.method == 'POST':
        form = RecipeForm()
        formset = RecipeFormSet
        return render(
            request,
            'recipes/recipe_new.html',
            {'form': form, 'is_edit': False, 'formset': formset},
        )

    form = RecipeForm(
        request.POST,
        files=request.FILES or None,
    )
    formset = RecipeFormSet(
        request.POST,
    )
    if form.is_valid():
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.pub_date = datetime.now()
        formset = RecipeFormSet(
            request.POST,
            instance=new_recipe,
        )
        if formset.is_valid():
            new_recipe.save()
            form.save_m2m()
            formset.save()
            return redirect('index')
    return render(
        request,
        'recipes/recipe_new.html',
        {'form': form, 'is_edit': False, 'formset': formset},
    )


    # recipe = form.save(commit=False)
    # recipe.author = request.user
    # recipe.pub_date = datetime.now()
    # recipe.save()
    # form.save_m2m()
    # return redirect('index')


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
    formset = RecipeFormSet(
        request.POST or None,
        instance=recipe,
    )
    if not request.method == 'POST':
        # return render(
        #     request,
        #     'recipes/recipe_new.html',
        #     {'recipe': recipe,
        #      'form': form,
        #      'is_edit': True
        #      }
        # )
        return render(
            request,
            'recipes/recipe_new.html',
            {'recipe': recipe,
             'form': form,
             'is_edit': True,
             'formset': formset
             },
        )

    if form.is_valid():
        # form.save()
        formset = RecipeFormSet(
            request.POST,
            instance=recipe,
        )
        if formset.is_valid():
            form.save()
            formset.save()
            return redirect('recipe', slug=form.cleaned_data.get("slug"))
    return render(
        request,
        'recipes/recipe_new.html',
        {'recipe': recipe,
         'form': form,
         'is_edit': True,
         'formset': formset,
         }
    )

    # if form.is_valid():
    #     new_recipe = form.save(commit=False)
    #     new_recipe.author = request.user
    #     new_recipe.pub_date = datetime.now()
    #     formset = RecipeFormSet(
    #         request.POST,
    #         instance=new_recipe,
    #     )
    #     if formset.is_valid():
    #         new_recipe.save()
    #         form.save_m2m()
    #         formset.save()
    #         return redirect('index')
    # return render(
    #     request,
    #     'recipes/recipe_new.html',
    #     {'form': form, 'is_edit': False, 'formset': formset},
    # )


def list_download(request):
    pass
