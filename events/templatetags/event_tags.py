from django import template

register = template.Library()

@register.filter
def get_username(value):
    return str(value).split('@')[0]