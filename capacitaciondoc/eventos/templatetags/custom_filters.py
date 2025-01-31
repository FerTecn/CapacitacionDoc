from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Obtiene el valor de una clave de un diccionario"""
    return dictionary.get(key)
