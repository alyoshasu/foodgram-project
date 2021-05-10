import io
from datetime import datetime

from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from foodgram.settings import RECIPES_PER_PAGE
from recipes.models import IngredientRecipe, Recipe
from users.models import Purchase

from .filters import RecipeFilter
from .forms import RecipeForm
from .utils import get_ingredients_dict, generate_dict, \
    render_ingredients_dict_for_edit, create_ingredients_objs, \
    render_ingredients_dict_for_new, ingredients_check

User = get_user_model()


def index(request):
    recipe_list = Recipe.objects.all()
    filtered_recipes = RecipeFilter(
        request.GET,
        queryset=recipe_list,
    )

    paginator = Paginator(filtered_recipes.qs, RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        "index.html",
        {
            'page': page,
            'paginator': paginator,
        },
    )


def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_recipes = user.recipes.all()
    filtered_recipes = RecipeFilter(
        request.GET,
        queryset=user_recipes,
    )

    paginator = Paginator(filtered_recipes.qs, RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'index.html',
        {
            'author': user,
            'page': page,
            'paginator': paginator,
        },
    )


@login_required
def favorite(request):
    favorite_list = Recipe.objects.filter(liked__user=request.user)
    filtered_recipes = RecipeFilter(
        request.GET,
        queryset=favorite_list,
    )

    paginator = Paginator(filtered_recipes.qs, RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'index.html',
        {
            'page': page,
            'paginator': paginator,
            'favorites': True,
        },
    )


def recipe(request, slug):
    recipe_item = get_object_or_404(Recipe, slug=slug)
    ingredients = IngredientRecipe.objects.filter(recipe=recipe_item)

    return render(
        request,
        "recipes/recipe_view.html",
        {
            'recipe': recipe_item,
            'ingredients': ingredients,
        },
    )


@login_required
def follow(request):
    follow_list = User.objects.filter(following__user=request.user)
    paginator = Paginator(follow_list, RECIPES_PER_PAGE)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(
        request,
        'authors/follow.html',
        {
            'page': page,
            'paginator': paginator
        },
    )


@login_required
def recipe_new(request):
    if not request.method == 'POST':
        form = RecipeForm()

        return render(
            request,
            'recipes/recipe_new.html',
            {
                'form': form,
                'is_edit': False
            },
        )

    form = RecipeForm(
        request.POST,
        request.FILES or None,
    )

    request_post = request.POST
    ingredients_dict = get_ingredients_dict(
        request_post,
    )

    ingredients = render_ingredients_dict_for_new(ingredients_dict)

    ingredient_error = ingredients_check(ingredients)

    if not form.is_valid() or ingredient_error:
        return render(
            request,
            'recipes/recipe_new.html',
            {
                'form': form,
                'is_edit': False,
                'ingredients': ingredients,
                'ingredient_error': ingredient_error,
            },
        )

    with transaction.atomic():
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.pub_date = datetime.now()
        new_recipe.save()
        ingredients_dict = get_ingredients_dict(
            request_post,
        )
        ingredients = create_ingredients_objs(new_recipe, ingredients_dict)
        IngredientRecipe.objects.bulk_create(
            ingredients
        )
        form.save_m2m()

    return redirect(
        'recipe',
        slug=form.cleaned_data.get("slug")
    )


@login_required
def recipe_edit(request, slug):
    edit_recipe = get_object_or_404(Recipe, slug=slug)
    if not edit_recipe.author == request.user:
        return redirect('recipe', slug=slug)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=edit_recipe,
    )

    ingredient_list = IngredientRecipe.objects.filter(recipe=edit_recipe)

    if not request.method == 'POST':
        ingredients = render_ingredients_dict_for_edit(ingredient_list)
        return render(
            request,
            'recipes/recipe_new.html',
            {'recipe': edit_recipe,
             'form': form,
             'is_edit': True,
             'ingredients': ingredients,
             }
        )

    request_post = request.POST

    ingredients_dict = get_ingredients_dict(
        request_post,
    )

    ingredients = render_ingredients_dict_for_new(ingredients_dict)

    ingredient_error = ingredients_check(ingredients)

    if not form.is_valid() or ingredient_error:
        return render(
            request,
            'recipes/recipe_new.html',
            {'recipe': edit_recipe,
             'form': form,
             'is_edit': True,
             'ingredients': ingredients,
             'ingredient_error': ingredient_error,
             }
        )

    with transaction.atomic():
        ingredient_list.delete()
        ingredients_dict = get_ingredients_dict(
            request_post,
        )
        ingredients = create_ingredients_objs(edit_recipe, ingredients_dict)
        IngredientRecipe.objects.bulk_create(
            ingredients
        )
        form.save()

    return redirect(
        'recipe',
        slug=form.cleaned_data.get("slug")
    )


@login_required
def list_download(request):
    output_dict = generate_dict(request.user)
    pdfmetrics.registerFont(TTFont('DejaVuSerif', './DejaVuSerif.ttf'))

    buffer = io.BytesIO()

    p = canvas.Canvas(buffer)
    p.setFont("DejaVuSerif", 15)

    start = 800
    for key in output_dict.keys():
        ingredient_line = r'{} - {}, {};'.format(
            key,
            output_dict[key][0],
            output_dict[key][1]
        )
        p.drawString(50, start, ingredient_line)
        start -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    return FileResponse(
        buffer,
        as_attachment=True,
        filename='purchase_list.pdf'
    )


@login_required
def purchase(request):
    user = request.user
    purchases = Purchase.objects.filter(user=user)
    return render(
        request,
        'purchase/purchase.html',
        {'purchases': purchases},
    )


@login_required
def recipe_delete(request, slug):
    recipe_item = get_object_or_404(Recipe, slug=slug)
    if not request.user == recipe_item.author:
        return redirect(
            'recipe',
            slug=slug
        )
    recipe_item.delete()
    return redirect(
        'index',
    )
