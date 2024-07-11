from django import template
from products.models import Category

register = template.Library()

@register.inclusion_tag('frontpage/menu.html')
def menu():
    categories = Category.objects.all()
    return {'categories':categories}