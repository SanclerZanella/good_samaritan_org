from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm


def checkout(request):
    """
     Render checkout template
    """

    if 'cart' in request.session:
        cart = request.session.get('cart', {})
        order_form = OrderForm()

        context = {
            'order_form': order_form,
        }

        template = 'checkout/checkout.html'
        return render(request, template, context)

    else:
        messages.warning(request, "There's nothing in your cart at the moment")
        return redirect('products')
