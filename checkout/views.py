"""
Handle all views and functionalities related to checkouts and payments
"""

# Django tools
from django.shortcuts import (render, redirect,
                              reverse, get_object_or_404,
                              HttpResponse)
from django.template.loader import render_to_string
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings

# Models
from .models import Order, OrderLineItem, Sponsor
from products.models import Product, Parcel
from profiles.models import UserProfile
from djstripe.models import Product as Sponsorship
from djstripe.models import Price, Customer, Subscription, Plan

# Forms
from .forms import OrderForm, SponsorForm
from profiles.forms import UserProfileForm

# Context
from cart.contexts import cart_contents

# Python tools
import json

# PDF
from io import BytesIO
from xhtml2pdf import pisa

# Stripe
import stripe
import djstripe


@require_POST
def cache_checkout_data(request):
    """
    Cache information on stripe api when payment intent
    is created, saving on payment intent metadata
    """

    try:

        # Modify payment intent metadata if a products,
        # parcel or both has checked out
        if 'cart' in request.session:

            # Modify Payment Intent
            pid = request.POST.get('client_secret').split('_secret')[0]
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.PaymentIntent.modify(pid, metadata={
                'cart': json.dumps(request.session.get('cart', {})),
                'save_info': request.POST.get('save_info'),
                'username': request.user,
            })
            return HttpResponse(status=200)

        # Modify payment intent metadata if a
        # sponsorship (subscription) has checked out
        else:

            # Modify Payment Intent
            pid = request.POST.get('client_secret').split('_secret')[0]
            stripe.api_key = settings.STRIPE_SECRET_KEY
            stripe.PaymentIntent.modify(pid, metadata={
                'save_info': request.POST.get('save_info'),
                'username': request.user,
            })
            return HttpResponse(status=200)

    except Exception as e:

        # Rise any error
        messages.error(request, 'Sorry, your payment cannot be \
            processed right now. Please try again later.')

        return HttpResponse(content=e, status=400)


def checkout(request):
    """
     Render checkout template and handle
     payment creation
    """

    # Get cart products
    cart = request.session.get('cart', {})
    if not cart:
        # Raise error if there is not cart session
        messages.error(request,
                       "There's nothing in your cart at the moment")
        return redirect(reverse('products'))

    stripe_public_key = settings.STRIPE_PUBLIC_KEY
    stripe_secret_key = settings.STRIPE_SECRET_KEY

    if request.method == 'POST':
        cart = request.session.get('cart', {'products': {},
                                            'parcels': {},
                                            })

        # Distinguishes products and parcels
        cart_products = cart['products']
        cart_parcels = cart['parcels']

        # Form data and attribute to related form
        # class and object on db
        form_data = {
            'full_name': request.POST['full_name'],
            'email': request.POST['email'],
            'country': request.POST['country'],
            'town_or_city': request.POST['town_or_city'],
            'street_address1': request.POST['street_address1'],
            'street_address2': request.POST['street_address2'],
        }
        order_form = OrderForm(form_data)

        # If form is valid save data on db
        if order_form.is_valid():

            # Create an Order object on db
            order = order_form.save(commit=False)
            pid = request.POST.get('client_secret').split('_secret')[0]
            order.stripe_pid = pid
            order.original_cart = json.dumps(cart)
            order.save()

            # If there are parcels and products on cart, then
            # Create an Orderline object for each parcel and product
            if cart_parcels:

                # If there are Parcels and products in the cart
                # Create an Orderline object for each parcel and product

                # Save products
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

                # Save parcels
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

            # If there are just products on cart, then
            # Create an Orderline object for each product
            elif cart_products:

                # Save products to Orderline
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

            # If there are just parcels on cart, then
            # Create an Orderline object for each parcels
            elif cart_parcels:

                # Save parcel to Orderline
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

            # Get checkout form
            order_form = OrderForm()

            current_cart = cart_contents(request)
            total = current_cart['grand_total']
            stripe_total = round(total * 100)
            stripe.api_key = stripe_secret_key

            # Create Payment intent
            intent = stripe.PaymentIntent.create(
                amount=stripe_total,
                currency=settings.STRIPE_CURRENCY,
            )

            if request.user.is_authenticated:
                try:

                    # If user is logged in then pre populate form
                    # with user details
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
                # If user is not logged in then
                # render empty form
                order_form = OrderForm()

        except Exception:
            messages.error(request, "Is there any product in your cart?!")
            return redirect(reverse('products'))

    if not stripe_public_key:
        # Verify if stripe public key is missing
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
        # If user is logged in attach the user's profile to the order
        profile = UserProfile.objects.get(user=request.user)

        order.user_profile = profile
        order.save()

    # Save the user's info to profile
    if save_info:

        # Get data and set to related form and db
        profile_data = {
            'default_country': order.country,
            'default_town_or_city': order.town_or_city,
            'default_street_address1': order.street_address1,
            'default_street_address2': order.street_address2,
        }
        user_profile_form = UserProfileForm(profile_data, instance=profile)

        if user_profile_form.is_valid():
            # Save data to profile if form is valid
            user_profile_form.save()

    messages.success(request, f'Donation successfully processed! \
        Your Donation number is {order_number}. A confirmation \
        email will be sent to {order.email}.')

    # Delete Cart session
    if 'cart' in request.session:
        del request.session['cart']

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
    }

    return render(request, template, context)


def subscription(request, sponsor_id):
    """
    Handle subscription view
    """

    # Sponsor option, Sponsor price and Sponsor form
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

    if request.user.is_authenticated:
        # Verify if user is logged in, then check if
        # the user already has a sponsorship(subscription)

        user = UserProfile.objects.get(user=request.user)
        sponsor_exist = Sponsor.objects.filter(user_profile=user).exists()

        if sponsor_exist:
            # If user already has a sponsorship(subscription)
            # then verify if current sponsor option is the
            # same which user has

            sponsor = Sponsor.objects.get(user_profile=user)
            subs = Subscription.objects.get(customer=sponsor.customer)
            plan = Plan.objects.get(id=subs.plan.id)
            current_option = Sponsorship.objects.get(id=sponsor_id)
            current_sponsor = Sponsorship.objects.get(name=plan.product)

            if current_sponsor.name == current_option.name:
                # If current sponsor option is the same which user has
                # redirect to sponsorship page

                messages.warning(request,
                                 f"You're already sponsoring! Your current sponsorship\
                                    is {plan.product}. To change your current\
                                        sponsorship select another option.")
                return redirect('sponsorship')

            else:
                # If current sponsor option is not the same which user has
                # then go to sponsorship(subscription) form page

                return render(request, template, context)

        else:
            # If user has not a sponsorship(subscription)
            # then go to sponsorship(subscription) form page

            return render(request, template, context)

    else:
        # If user is not logged in
        # then go to sponsorship(subscription) form page

        return render(request, template, context)


@require_POST
def subscription_checkout(request):
    """
    Handle subscription checkout creating a customer
    and a subscription
    """

    if request.method == 'POST':
        data = json.loads(request.body)
        payment_method = data['payment_method']
        data_form = data['data_form']
        sponsor_id = data_form['productId']
        email = data_form['email']
        stripe.api_key = djstripe.settings.STRIPE_SECRET_KEY

        payment_method_obj = stripe.PaymentMethod.retrieve(payment_method)
        djstripe.models.PaymentMethod.sync_from_stripe_data(payment_method_obj)

        # Verify if user is logged
        if request.user.is_authenticated:
            user = UserProfile.objects.get(user=request.user)
            sponsor_exist = Sponsor.objects.filter(user_profile=user).exists()

            # Verify if there is a sponsor object for this user on db
            if sponsor_exist:
                sponsor = Sponsor.objects.get(user_profile=user)
                subscrip = Subscription.objects.get(customer=sponsor.customer)
                plan = Plan.objects.get(id=subscrip.plan)

                # Sponsorship(subscription) option chosen on sponsorship page
                current_option = Sponsorship.objects.get(id=sponsor_id)

                # Current user's sponsorship(subscription) on db
                current_sponsor = Sponsorship.objects.get(name=plan.product)

                # If there is a sponsor object for this user on db
                # then verify if the chosen sponsorship is the same
                # as current user's sponsorship using the user name
                if current_sponsor.name == current_option.name:

                    # If the chosen sponsorship is the same as
                    # the current user's sponsorship
                    # then redirect to sponsorship page
                    # Allowing just one sponsorship(subscription) per user
                    messages.warning(request,
                                     f"You're already sponsoring! Your current sponsorship\
                                     is {plan.product}. To change your current\
                                        sponsorship select another option.")
                    return redirect('sponsorship')
                else:

                    # If the chosen sponsorship is not the same as
                    # the current user's sponsorship
                    # then delete the old sponsorship and
                    # add the new one
                    stripe.api_key = settings.STRIPE_SECRET_KEY
                    stripe.Customer.delete(sponsor.customer.id)

                    Sponsor.objects.filter(customer=sponsor.customer).delete()
                    Customer.objects.filter(id=sponsor.customer.id).delete()

                    try:
                        # This creates a new Customer and attaches the
                        # PaymentMethod in one API call.
                        customer = stripe.Customer.create(
                            payment_method=payment_method,
                            email=email,
                            invoice_settings={
                                'default_payment_method': payment_method
                            }
                        )

                        djstripe_model = djstripe.models.Customer
                        ct = djstripe_model.sync_from_stripe_data(customer)

                        subs = stripe.Subscription.create(
                            customer=customer.id,
                            items=[
                                {
                                    "price": data["price_id"],
                                },
                            ],
                            expand=["latest_invoice.payment_intent"],
                            metadata={
                                'save_info': data_form['save_info'],
                                'username': request.user,
                                'name': str(data_form['name']),
                                'email': str(data_form['email']),
                                'line1': str(data_form['address1']),
                                'line2': str(data_form['address2']),
                                'city': str(data_form['town_or_city']),
                                'country': str(data_form['country'])
                            }
                        )

                        dj_sub_model = djstripe.models.Subscription
                        dj_sub = dj_sub_model.sync_from_stripe_data(subs)
                        plan = Plan.objects.get(id=subs.plan.id)

                        sponsor = Sponsor(
                            customer=ct,
                            subscription=dj_sub,
                            full_name=data_form['name'],
                            email=data_form['email'],
                            country=data_form['country'],
                            town_or_city=data_form['town_or_city'],
                            street_address1=data_form['address1'],
                            street_address2=data_form['address2'],
                            grand_total=plan.amount
                        )
                        sponsor.save()

                        return redirect(reverse('subscription_success',
                                                args=[sponsor.customer]))
                    except Exception as e:
                        return JsonResponse({'error': (e.args[0])}, status=403)

            else:

                # If there is not a Sponsor object for the user on db
                # then create one for the user
                try:
                    # This creates a new Customer and attaches the
                    # PaymentMethod in one API call.
                    customer = stripe.Customer.create(
                        payment_method=payment_method,
                        email=email,
                        invoice_settings={
                            'default_payment_method': payment_method
                        }
                    )

                    djstripe_model = djstripe.models.Customer
                    ct = djstripe_model.sync_from_stripe_data(customer)

                    subs = stripe.Subscription.create(
                        customer=customer.id,
                        items=[
                            {
                                "price": data["price_id"],
                            },
                        ],
                        expand=["latest_invoice.payment_intent"],
                        metadata={
                            'save_info': data_form['save_info'],
                            'username': request.user,
                            'name': str(data_form['name']),
                            'email': str(data_form['email']),
                            'line1': str(data_form['address1']),
                            'line2': str(data_form['address2']),
                            'city': str(data_form['town_or_city']),
                            'country': str(data_form['country'])
                        }
                    )

                    dj_sub = djstripe.models.Subscription
                    djstripe_subscription = dj_sub.sync_from_stripe_data(subs)
                    plan = Plan.objects.get(id=subs.plan.id)

                    sponsor = Sponsor(
                        customer=ct,
                        subscription=djstripe_subscription,
                        full_name=data_form['name'],
                        email=data_form['email'],
                        country=data_form['country'],
                        town_or_city=data_form['town_or_city'],
                        street_address1=data_form['address1'],
                        street_address2=data_form['address2'],
                        grand_total=plan.amount
                    )
                    sponsor.save()

                    return redirect(reverse('subscription_success',
                                            args=[sponsor.customer]))
                except Exception as e:
                    return JsonResponse({'error': (e.args[0])}, status=403)

        else:

            # If the user is not logged, then verify if
            # there is a sponsor object for the anonymous user
            # on db, using email provided on form
            sponsor_exist = Sponsor.objects.filter(email=email).exists()

            if sponsor_exist:
                an_sponsor = Sponsor.objects.get(email=email)
                gsub = Subscription.objects.get(customer=an_sponsor.customer)
                subscrip = gsub
                plan = Plan.objects.get(id=subscrip.plan)

                # Sponsorship(subscription) option chosen on sponsorship page
                current_option = Sponsorship.objects.get(id=sponsor_id)

                # Current user's sponsorship(subscription) on db
                current_sponsor = Sponsorship.objects.get(name=plan.product)

                # If there is a sponsor object for this user on db
                # then verify if the chosen sponsorship is the same
                # as current user's sponsorship using the user name
                if current_sponsor.name == current_option.name:

                    # If the chosen sponsorship is the same as
                    # the current user's sponsorship
                    # then redirect to sponsorship page
                    # Allowing just one sponsorship(subscription) per user
                    return redirect(reverse('subscription',
                                            args=[sponsor_id]))

                else:

                    # If the chosen sponsorship is not the same as
                    # the current user's sponsorship
                    # then delete the old sponsorship and
                    # add the new one
                    stripe.api_key = settings.STRIPE_SECRET_KEY
                    stripe.Customer.delete(an_sponsor.customer.id)

                    sponsorob = Sponsor.objects
                    sponsorob.filter(customer=an_sponsor.customer).delete()
                    Customer.objects.filter(id=an_sponsor.customer.id).delete()

                    try:
                        # This creates a new Customer and attaches the
                        # PaymentMethod in one API call.
                        customer = stripe.Customer.create(
                            payment_method=payment_method,
                            email=email,
                            invoice_settings={
                                'default_payment_method': payment_method
                            }
                        )

                        djstripe_model = djstripe.models.Customer
                        ct = djstripe_model.sync_from_stripe_data(customer)

                        subs = stripe.Subscription.create(
                            customer=customer.id,
                            items=[
                                {
                                    "price": data["price_id"],
                                },
                            ],
                            expand=["latest_invoice.payment_intent"],
                            metadata={
                                'save_info': data_form['save_info'],
                                'username': request.user,
                                'name': str(data_form['name']),
                                'email': str(data_form['email']),
                                'line1': str(data_form['address1']),
                                'line2': str(data_form['address2']),
                                'city': str(data_form['town_or_city']),
                                'country': str(data_form['country'])
                            }
                        )

                        submodel = djstripe.models.Subscription
                        dj_sub = submodel.sync_from_stripe_data(subs)
                        plan = Plan.objects.get(id=subs.plan.id)

                        sponsor = Sponsor(
                            customer=ct,
                            subscription=dj_sub,
                            full_name=data_form['name'],
                            email=data_form['email'],
                            country=data_form['country'],
                            town_or_city=data_form['town_or_city'],
                            street_address1=data_form['address1'],
                            street_address2=data_form['address2'],
                            grand_total=plan.amount
                        )
                        sponsor.save()

                        return redirect(reverse('subscription_success',
                                                args=[sponsor.customer]))

                    except Exception as e:
                        return JsonResponse({'error': (e.args[0])}, status=403)

            else:

                # If there is not a Sponsor object for the user on db
                # then create one for the user
                try:
                    # This creates a new Customer and attaches the
                    # PaymentMethod in one API call.
                    customer = stripe.Customer.create(
                        payment_method=payment_method,
                        email=email,
                        invoice_settings={
                            'default_payment_method': payment_method
                        }
                    )

                    djstripe_model = djstripe.models.Customer
                    ct = djstripe_model.sync_from_stripe_data(customer)

                    subs = stripe.Subscription.create(
                        customer=customer.id,
                        items=[
                            {
                                "price": data["price_id"],
                            },
                        ],
                        expand=["latest_invoice.payment_intent"],
                        metadata={
                            'save_info': data_form['save_info'],
                            'username': request.user,
                            'name': str(data_form['name']),
                            'email': str(data_form['email']),
                            'line1': str(data_form['address1']),
                            'line2': str(data_form['address2']),
                            'city': str(data_form['town_or_city']),
                            'country': str(data_form['country'])
                        }
                    )

                    dj_sub = djstripe.models.Subscription
                    djstripe_subscription = dj_sub.sync_from_stripe_data(subs)
                    plan = Plan.objects.get(id=subs.plan.id)

                    sponsor = Sponsor(
                        customer=ct,
                        subscription=djstripe_subscription,
                        full_name=data_form['name'],
                        email=data_form['email'],
                        country=data_form['country'],
                        town_or_city=data_form['town_or_city'],
                        street_address1=data_form['address1'],
                        street_address2=data_form['address2'],
                        grand_total=plan.amount
                    )
                    sponsor.save()

                    return redirect(reverse('subscription_success',
                                            args=[sponsor.customer]))
                except Exception as e:
                    return JsonResponse({'error': (e.args[0])}, status=403)

    else:
        return HttpResponse(status=500)


def subscription_success(request, customer_id):
    """
    Handle successful subscriptions
    """

    save_info = request.session.get('save_info')
    customer_data = get_object_or_404(Customer, id=customer_id)
    sponsor = get_object_or_404(Sponsor, customer=customer_data)

    if request.user.is_authenticated:

        # If the user is logged, then update Sponsor object
        # Add user object from db
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
        'sponsor': sponsor,
    }

    return render(request, template, context)


def render_pdf(request, order_number):
    """
    Create pdf with donation details after checkout
    """

    order_type = order_number.split('_')[0]

    if order_type == 'cus':
        customer_data = get_object_or_404(Customer, id=order_number)
        order = get_object_or_404(Sponsor, customer=customer_data)

    else:
        order = get_object_or_404(Order, order_number=order_number)

    path = 'checkout/document/checkout_success_print.html'
    context = {
        'order': order,
    }

    # Convert HTML to byte string
    html = render_to_string(path, context)
    io_bytes = BytesIO()

    # Convert string to PDF
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), io_bytes)

    if not pdf.err:
        return HttpResponse(io_bytes.getvalue(),
                            content_type='application/pdf')
    else:
        return HttpResponse("Error while rendering PDF", status=400)
