import os
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import OrderForm
if os.path.exists('env.py'):
    import env


def checkout(request):
    """
     Render checkout template
    """

    if 'cart' in request.session:
        cart = request.session.get('cart', {})
        order_form = OrderForm()
        stripe_public_key = os.environ.get('STRIPE_PUBLIC_KEY', '')
        client_secret = os.environ.get('CLIENT_SECRET', '')

        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': client_secret,
        }

        template = 'checkout/checkout.html'
        return render(request, template, context)

    else:
        messages.warning(request, "There's nothing in your cart at the moment")
        return redirect('products')
