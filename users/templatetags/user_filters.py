from django import template

from users.models import Favorite, Subscription, Purchase

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


@register.filter
def is_purchase(recipe, user):
    if not Purchase.objects.filter(recipe=recipe, user=user):
        return False
    return Purchase.objects.get(recipe=recipe, user=user).id


@register.filter
def is_subscribed(author, user):
    if not Subscription.objects.filter(author=author, user=user):
        return False
    return Subscription.objects.get(author=author, user=user).id

