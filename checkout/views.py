from django.shortcuts import render, redirect
from django.contrib import messages
import stripe


def checkout_view(request):
    """
     Render checkout template
    """

    if 'cart' in request.session:
        cart = request.session.get('cart', {})

        template = 'checkout/checkout.html'
        return render(request, template)

    else:
        messages.warning(request, 'There is no product to\
        check out at the moment.')
        return redirect('view_cart')
