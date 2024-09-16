from django import template

register = template.Library()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key, "")


@register.filter
def subtract(value, arg):
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return ""


@register.filter
def split_by_period(value):
    """Splits a string by '.' and returns a list of sentences."""
    if isinstance(value, str):
        return [sentence.strip() for sentence in value.split(".") if sentence.strip()]
    return []
