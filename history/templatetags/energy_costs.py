from django import template

from history.cost import Cost
from history.models import History

register = template.Library()


@register.simple_tag(name='energy_cost')
def energy_cost(value: History, cost: Cost, price_day: float, price_night: float):
    return round(cost.price(value.start, price_day, price_night) * value.energy, 2)
