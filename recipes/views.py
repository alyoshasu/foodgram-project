from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect

from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

from recipes.models import Recipe, IngredientRecipe, Ingredient

from datetime import datetime

from users.models import Purchase
from .filters import RecipeFilter
from .forms import RecipeForm

import io
from django.http import FileResponse

User = get_user_model()


def index(request):
    recipe_list = Recipe.objects.all()
    filtered_recipes = RecipeFilter(
        request.GET,
        queryset=recipe_list,
    )

    paginator = Paginator(filtered_recipes.qs, 6)
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

    paginator = Paginator(filtered_recipes.qs, 6)
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

    paginator = Paginator(filtered_recipes.qs, 6)
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
    paginator = Paginator(follow_list, 6)
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
        files=request.FILES or None,
    )

    if not form.is_valid():
        return render(
            request,
            'recipes/recipe_new.html',
            {
                'form': form,
                'is_edit': False,
            },
        )

    with transaction.atomic():
        new_recipe = form.save(commit=False)
        new_recipe.author = request.user
        new_recipe.pub_date = datetime.now()
        request_post = request.POST
        new_recipe.save()
        get_ingredients(new_recipe, request_post)
        form.save_m2m()

    return redirect(
        'recipe',
        slug=form.cleaned_data.get("slug")
    )


def get_ingredients(recipe_item, post_request):
    ingredients_index = []

    for key in post_request.keys():
        if 'nameIngredient_' in str(key):
            ingredients_index.append(key[15:])

    for i in ingredients_index:
        ingredient = get_object_or_404(Ingredient, title=post_request['nameIngredient_' + i])
        quantity = post_request['valueIngredient_' + i]
        recipe_item.ingredients.add(ingredient, through_defaults={'quantity': quantity})


@login_required
def recipe_edit(request, slug):
    edit_recipe = get_object_or_404(Recipe, slug=slug)
    ingredient_list = IngredientRecipe.objects.filter(recipe=edit_recipe)
    ingredients = render_ingredients_list(ingredient_list)
    if not edit_recipe.author == request.user:
        return redirect('recipe', slug=slug)
    form = RecipeForm(
        request.POST or None,
        files=request.FILES or None,
        instance=edit_recipe,
    )

    if not request.method == 'POST':
        return render(
            request,
            'recipes/recipe_new.html',
            {'recipe': edit_recipe,
             'form': form,
             'is_edit': True,
             'ingredients': ingredients,
             }
        )

    if not form.is_valid():
        return render(
            request,
            'recipes/recipe_new.html',
            {'recipe': edit_recipe,
             'form': form,
             'is_edit': True,
             }
        )

    with transaction.atomic():
        ingredient_list.delete()
        request_post = request.POST
        get_ingredients(edit_recipe, request_post)
        form.save()

    return redirect(
        'recipe',
        slug=form.cleaned_data.get("slug")
    )


def render_ingredients_list(ingredient_list):
    ingredients = {}
    for i in range(len(ingredient_list)):
        ingredients[str(i+1)] = [
            ingredient_list[i].ingredient.title,
            ingredient_list[i].quantity,
            ingredient_list[i].ingredient.dimension
        ]
    return ingredients


@login_required
def list_download(request):
    output_dict = generate_dict(request.user)
    pdfmetrics.registerFont(TTFont('DejaVuSerif', './DejaVuSerif.ttf'))

    # Create a file-like buffer to receive PDF data.
    buffer = io.BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer)
    p.setFont("DejaVuSerif", 15)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # See the ReportLab documentation for the full list of functionality.
    start = 800
    for key in output_dict.keys():
        ingredient_line = r'{} - {}, {};'.format(key, output_dict[key][0], output_dict[key][1])
        p.drawString(50, start, ingredient_line)
        start -= 20

    # Close the PDF object cleanly, and we're done.
    p.showPage()
    p.save()

    # FileResponse sets the Content-Disposition header so that browsers
    # present the option to save the file.
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='purchase_list.pdf')


def generate_dict(user):
    ingredients_quantity = {}
    for purchase_item in user.purchases.all():
        recipe_item = purchase_item.recipe
        for ingredient_item in recipe_item.ingredients.all():
            quantity = IngredientRecipe.objects.get(
                    recipe=recipe_item,
                    ingredient=ingredient_item
                ).quantity
            if ingredient_item.title in ingredients_quantity.keys():
                ingredients_quantity[ingredient_item.title][0] += quantity
            else:
                ingredients_quantity[ingredient_item.title] = [quantity, ingredient_item.dimension]

    return ingredients_quantity


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
