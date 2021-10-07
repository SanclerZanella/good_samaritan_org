from django import template


register = template.Library()


@register.filter(name='calc_subtotal')
def calc_subtotal(price, quantity):
    """
    Calculate Subtotal per product
    Subtotal = unit price * product quantity
    """

    return price * quantity


@register.filter
def addstr(arg1, arg2):
    """
    concatenate arg1 & arg2
    """

    return str(arg1) + str(arg2)
