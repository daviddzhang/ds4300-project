from django import template
from events.models import Address

register = template.Library()

@register.simple_tag
def render_location(address):
    return Address.address_map_to_string(address)

@register.simple_tag
def render_date(date):
    print(date)
    return date.strftime("%m/%d/%Y at %I:%M%p")
