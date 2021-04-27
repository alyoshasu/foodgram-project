import django_filters

from recipes.models import Recipe


class RecipeFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Recipe
        fields = ['tags']
