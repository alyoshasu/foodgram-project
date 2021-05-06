import json

from django.core.management.base import BaseCommand

from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'Uploading Ingredients data-set'

    def handle(self, *args, **options):
        with open(
                './recipes/management/commands/ingredients.json'
        ) as json_file:
            ingredients = json.load(json_file)
            for ingredient in ingredients:
                title, dimension = ingredient['title'], ingredient['dimension']
                Ingredient.objects.get_or_create(
                    title=title,
                    dimension=dimension
                )
