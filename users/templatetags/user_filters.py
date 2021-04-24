from django import template

from users.models import Favorite

register = template.Library()


@register.filter
def addclass(field, css):
    return field.as_widget(attrs={"class": css})


# @register.filter
# def userfilter(objects, user):
# 	return objects.filter(user=user)

@register.filter
def is_favorite(recipe, user):
    if not Favorite.objects.filter(recipe=recipe, user=user):
        return False
    return Favorite.objects.get(recipe=recipe, user=user).id
