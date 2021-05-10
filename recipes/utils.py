from django.shortcuts import get_object_or_404

from recipes.models import IngredientRecipe, Ingredient


def get_ingredients_dict(post_request):
    ingredients = {}

    for key, name in post_request.items():
        if key.startswith('nameIngredient'):
            num = key.partition('_')[-1]
            ingredients[name] = post_request[f'valueIngredient_{num}']

    return ingredients


def create_ingredients_objs(recipe_item, ingredients):
    objs = []

    for name, quantity in ingredients.items():

        ingredient = get_object_or_404(
            Ingredient,
            title=name,
        )
        objs.append(
            IngredientRecipe(
                recipe=recipe_item,
                ingredient=ingredient,
                quantity=quantity,
            )
        )

    return objs


def render_ingredients_dict_for_edit(ingredient_list):
    ingredients = {}
    for i in range(len(ingredient_list)):
        ingredients[str(i+1)] = [
            ingredient_list[i].ingredient.title,
            ingredient_list[i].quantity,
            ingredient_list[i].ingredient.dimension
        ]
    return ingredients


def render_ingredients_dict_for_new(ingredients_dict):
    k = 1
    ingredients = {}
    for key in ingredients_dict.keys():
        dimension = get_object_or_404(Ingredient, title=key).dimension
        ingredients[k] = [key, ingredients_dict[key], dimension]
        k += 1
    return ingredients


def ingredients_check(ingredients):
    for key in ingredients.keys():
        if int(ingredients[key][1]) <= 0:
            return True
    return False


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
                ingredients_quantity[ingredient_item.title] = [
                    quantity,
                    ingredient_item.dimension
                ]

    return ingredients_quantity
