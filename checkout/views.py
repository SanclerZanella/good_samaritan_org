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
from .forms import OrderForm, SponsorForm
from .models import Order, OrderLineItem, Sponsor
import json
from django.http import JsonResponse
from profiles.models import UserProfile
from profiles.forms import UserProfileForm
import djstripe
from djstripe.models import Product as Sponsorship
from djstripe.models import Price, Customer


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

    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request,
                       "There's nothing in your cart at the moment")
        return redirect(reverse('products'))

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

            if cart_parcels:

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

        try:
            order_form = OrderForm()

            current_cart = cart_contents(request)
            total = current_cart['grand_total']
            stripe_total = round(total * 100)
            stripe.api_key = stripe_secret_key

            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )

            if request.user.is_authenticated:
                try:
                    profile = UserProfile.objects.get(user=request.user)
                    order_form = OrderForm(initial={
                        'full_name': profile.user.get_full_name(),
                        'email': profile.user.email,
                        'country': profile.default_country,
                        'town_or_city': profile.default_town_or_city,
                        'street_address1': profile.default_street_address1,
                        'street_address2': profile.default_street_address2,
                    })
                except UserProfile.DoesNotExist:
                    order_form = OrderForm()
            else:
                order_form = OrderForm()

        except Exception as e:
            messages.error(request, "Is there any product in your cart?!")
            return redirect(reverse('products'))

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

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        # Attach the user's profile to the order
        order.user_profile = profile
        order.save()

    # Save the user's info
    if save_info:
        profile_data = {
            'default_country': order.country,
            'default_town_or_city': order.town_or_city,
            'default_street_address1': order.street_address1,
            'default_street_address2': order.street_address2,
        }
        user_profile_form = UserProfileForm(profile_data, instance=profile)
        if user_profile_form.is_valid():
            user_profile_form.save()

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


def subscription(request, sponsor_id):

    sponsor_prod = Sponsorship.objects.get(id=sponsor_id)
    sponsor_price = Price.objects.get(product=sponsor_id)
    form = SponsorForm()

    stripe_public_key = settings.STRIPE_PUBLIC_KEY

    context = {
        'sponsor': sponsor_prod,
        'form': form,
        'stripe_public_key': stripe_public_key,
        'price': sponsor_price,
    }

    template = 'checkout/subscription.html'
    return render(request, template, context)


def subscription_checkout(request):

    if request.method == 'POST':
        data = json.loads(request.body)
        payment_method = data['payment_method']
        data_form = data['data_form']
        email = data_form['email']
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

        payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
        djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

        try:
            # This creates a new Customer and attaches the PaymentMethod in one API call.
            customer = stripe.Customer.create(
                payment_method=payment_method,
                email=email,
                invoice_settings={
                    'default_payment_method': payment_method
                }
            )

            ct = djstripe.models.Customer.sync_from_stripe_data(customer)
            print('HERE!!!')
            print(data)

            subs = stripe.Subscription.create(
                customer=customer.id,
                items=[
                    {
                        "price": data["price_id"],
                    },
                ],
                expand=["latest_invoice.payment_intent"]
            )

            dj_sub = djstripe.models.Subscription
            djstripe_subscription = dj_sub.sync_from_stripe_data(subs)

            sponsor = Sponsor(
                customer=ct,
                subscription=djstripe_subscription,
                full_name=data_form['name'],
                email=data_form['email'],
                country=data_form['country'],
                town_or_city=data_form['town_or_city'],
                street_address1=data_form['address1'],
                street_address2=data_form['address2'],
                grand_total=50.00
            )
            sponsor.save()

            return redirect(reverse('subscription_success', args=[sponsor.customer]))

        except Exception as e:
            return JsonResponse({'error': (e.args[0])}, status =403)
    else:
        return HttpResponse(status=500)


def subscription_success(request, customer_id):
    save_info = request.session.get('save_info')
    customer_data = get_object_or_404(Customer, id=customer_id)
    sponsor = get_object_or_404(Sponsor, customer=customer_data)

    if request.user.is_authenticated:
        profile = UserProfile.objects.get(user=request.user)
        
        # Attach the user's profile to the sponsor
        sponsor.user_profile = profile
        sponsor.save()

    # Save the user's info
    if save_info:
        profile_data = {
            'default_country': sponsor.country,
            'default_town_or_city': sponsor.town_or_city,
            'default_street_address1': sponsor.street_address1,
            'default_street_address2': sponsor.street_address2,
        }
        user_profile_form = UserProfileForm(profile_data, instance=profile)
        if user_profile_form.is_valid():
            user_profile_form.save()

    messages.success(request, 'Thank you for you sponsorship!')

    template = 'checkout/subscription_success.html'
    context = {
        'sponsor': 'sponsor',
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
