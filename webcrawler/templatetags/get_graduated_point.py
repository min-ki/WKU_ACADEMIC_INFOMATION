from django import template

register = template.Library()

@register.filter
def keyvalue(dict, key):

    if dict.get(key):
        return dict[key]
    return 0