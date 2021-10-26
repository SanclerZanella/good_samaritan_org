from django import template
from django.shortcuts import get_object_or_404
from djstripe.models import Plan


register = template.Library()


@register.filter(name='sponsor_price')
def get_sponsor_price(sponsor_id):
    """
    Get sponsor price
    """

    sponsor = get_object_or_404(Plan, product=sponsor_id)
    sponsor_price = int(sponsor.amount)

    return sponsor_price
