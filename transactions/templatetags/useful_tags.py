from django import template
from django.template import defaultfilters

register = template.Library()

@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def not_none(value):
    return value if value != None else ''

@register.filter
def nice_date(value):
    return defaultfilters.date(value, "d M Y")

@register.filter
def excel_date(value):
    return defaultfilters.date(value, "d/m/y")

