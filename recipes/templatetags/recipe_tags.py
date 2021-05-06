from django import template

register = template.Library()


@register.simple_tag()
def my_url(value, field_name, urlencode=None):
    url = '?{}={}'.format(field_name, value)

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(
            lambda p: p.split('=')[0] != field_name,
            querystring
        )
        encoded_querystring = '&'.join(filtered_querystring)
        url = '{}&{}'.format(url, encoded_querystring)

    return url


@register.simple_tag()
def add_tag(value, field_name, urlencode=None, add=True):
    url = '?{}={}'.format(field_name, value)

    if urlencode:
        querystring = urlencode.split('&')
        filtered_querystring = filter(
            lambda p: p.split('=') != [field_name, str(value)],
            querystring
        )
        encoded_querystring = '&'.join(filtered_querystring)
        if add:
            url = '{}&{}'.format(url, encoded_querystring)
        else:
            url = '?{}'.format(encoded_querystring)

    return url


@register.filter
def tag_chosen(urlencode, tag):
    return True if 'tags={}'.format(tag) in urlencode else False
