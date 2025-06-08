from django import template
from urllib.parse import urlencode

register = template.Library()


@register.filter
def currency(value, currency_symbol="LKR"):
    """
    Converts a number to a string with a currency symbol.
    """
    try:
        value = float(value)
        return f"{currency_symbol} {value:,.2f}"
    except (ValueError, TypeError):
        return value


@register.simple_tag(takes_context=True)
def toggle_tag_url(context, tag_slug):
    request = context["request"]
    get_copy = request.GET.copy()

    tags = get_copy.get("tags", "")
    tag_list = tags.split(",") if tags else []

    if tag_slug in tag_list:
        tag_list.remove(tag_slug)
    else:
        tag_list.append(tag_slug)

    # Clean empty strings
    tag_list = list(filter(None, tag_list))
    if tag_list:
        get_copy["tags"] = ",".join(tag_list)
    else:
        get_copy.pop("tags", None)

    return "?" + urlencode(get_copy, doseq=True)
