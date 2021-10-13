from django.shortcuts import (render, redirect,
                              reverse, get_object_or_404,
                              HttpResponse)
from django.contrib import messages
from django.conf import settings
from io import BytesIO
import stripe
from xhtml2pdf import pisa
from django.template.loader import render_to_string
from products.models import Product, Parcel
from cart.contexts import cart_contents
from django.views.decorators.http import require_POST
from .forms import OrderForm
from .models import Order, OrderLineItem
import json


@require_POST
def cache_checkout_data(request):
    try:
        pid = request.POST.get('client_secret').split('_secret')[0]
        stripe.api_key = settings.STRIPE_SECRET_KEY
        stripe.PaymentIntent.modify(pid, metadata={
            'cart': json.dumps(request.session.get('cart', {})),
            'save_info': request.POST.get('save_info'),
            'username': request.user,
        })
        return HttpResponse(status=200)
    except Exception as e:
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')
        return HttpResponse(content=e, status=400)


def checkout(request):
    """
     Render checkout template
    """

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {'products': {},
                                            'parcels': {},
                                            })
        cart_products = cart['products']
        cart_parcels = cart['parcels']

        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'country': request.POST['country'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
        }
        order_form = OrderForm(form_data)

        if order_form.is_valid():
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()

            if cart_parcels and cart_parcels:

                for item_id, item_data in cart_products.items():

                    try:
                        product = Product.objects.get(id=item_id)

                        if isinstance(item_data, int):
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                parcel=None,
                                quantity=item_data,
                                )
                            order_line_item.save()
                    except Exception:
                        messages.error(request, (
                                "One of the products in your cart wasn't found\
                                    in our database. "
                                "Please call us for assistance!")
                                )
                        order.delete()
                        return redirect(reverse('view_cart'))

                for item_id, item_data in cart_parcels.items():

                    try:
                        parcel = Parcel.objects.get(id=item_id)

                        if isinstance(item_data, int):
                            order_line_item = OrderLineItem(
                                order=order,
                                product=None,
                                parcel=parcel,
                                quantity=item_data,
                                )
                            order_line_item.save()
                    except Exception:
                        messages.error(request, (
                                "One of the parcels in your cart wasn't found\
                                    in our database. "
                                "Please call us for assistance!")
                                )
                        order.delete()
                        return redirect(reverse('view_cart'))

            elif cart_products:

                for item_id, item_data in cart_products.items():

                    try:
                        product = Product.objects.get(id=item_id)

                        if isinstance(item_data, int):
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                parcel=None,
                                quantity=item_data,
                                )
                            order_line_item.save()
                    except Exception:
                        messages.error(request, (
                                "One of the products in your cart wasn't found\
                                    in our database. "
                                "Please call us for assistance!")
                                )
                        order.delete()
                        return redirect(reverse('view_cart'))

            elif cart_parcels:

                for item_id, item_data in cart_parcels.items():

                    try:
                        parcel = Parcel.objects.get(id=item_id)

                        if isinstance(item_data, int):
                            order_line_item = OrderLineItem(
                                order=order,
                                product=None,
                                parcel=parcel,
                                quantity=item_data,
                                )
                            order_line_item.save()
                    except Exception:
                        messages.error(request, (
                                "One of the parcels in your cart wasn't found\
                                    in our database. "
                                "Please call us for assistance!")
                                )
                        order.delete()
                        return redirect(reverse('view_cart'))

            request.session['save_info'] = 'save-info' in request.POST
            return redirect(reverse('checkout_success',
                            args=[order.order_number]))

        else:
            messages.error(request, 'There was an error with your form. \
                Please double check your information.')

    else:
        cart = request.session.get('cart', {})

        if not cart:
            messages.error(request,
                           "There's nothing in your cart at the moment")
            return redirect(reverse('products'))

        order_form = OrderForm()

        current_cart = cart_contents(request)
        total = current_cart['grand_total']
        stripe_total = round(total * 100)
        stripe.api_key = stripe_secret_key

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


def checkout_success(request, order_number):
    """
    Handle successful checkouts
    """
    save_info = request.session.get('save_info')
    order = get_object_or_404(Order, order_number=order_number)
    messages.success(request, f'Donation successfully processed! \
        Your Donation number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)


def render_pdf(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    path = 'checkout/document/checkout_success_print.html'
    context = {
        'order': order,
    }

    html = render_to_string(path, context)
    io_bytes = BytesIO()

    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)

    if not pdf.err:
        return HttpResponse(io_bytes.getvalue(), content_type='application/pdf')
    else:
        return HttpResponse("Error while rendering PDF", status=400)
