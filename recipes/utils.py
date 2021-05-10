from django.shortcuts import get_object_or_404

from recipes.models import IngredientRecipe, Ingredient


def get_ingredients(recipe_item, post_request):
    ingredients = {}

    for key, name in post_request.items():
        if key.startswith('nameIngredient'):
            num = key.partition('_')[-1]
            ingredients[name] = post_request[f'valueIngredient_{num}']

    objs = []

    for name, quantity in ingredients.items():
        if quantity <= 0:
            return False

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


def render_ingredients_list(ingredient_list):
    ingredients = {}
    for i in range(len(ingredient_list)):
        ingredients[str(i+1)] = [
            ingredient_list[i].ingredient.title,
            ingredient_list[i].quantity,
            ingredient_list[i].ingredient.dimension
        ]
    return ingredients


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
