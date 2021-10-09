import os
from django.shortcuts import render, redirect
from django.contrib import messages
from django.conf import settings
from .forms import OrderForm
from cart.contexts import cart_contents
import stripe
# if os.path.exists('env.py'):
#     import env


def checkout(request):
    """
     Render checkout template
    """

    if 'cart' in request.session:
        order_form = OrderForm()
        stripe_public_key = settings.STRIPE_PUBLIC_KEY
        client_secret = settings.STRIPE_SECRET_KEY

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = client_secret

        intent = stripe.PaymentIntent.create(
            amount=stripe_total,
            currency=settings.STRIPE_CURRENCY,
        )

        if not stripe_public_key:
            messages.warning(request, 'Stripe public key is missing. \
                Did you forget to set it in your environment?')

        context = {
            'order_form': order_form,
            'stripe_public_key': stripe_public_key,
            'client_secret': intent.client_secret,
        }

        template = 'checkout/checkout.html'
        return render(request, template, context)

    else:
        messages.warning(request, "There's nothing in your cart at the moment")
        return redirect('products')
