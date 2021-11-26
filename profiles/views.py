from django.shortcuts import (render, get_object_or_404, redirect)
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import UserProfile
from checkout.models import Sponsor
from djstripe.models import Subscription
from .forms import UserProfileForm, RedeemForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from checkout.models import Order


@login_required
def profile(request):
    """ Display the user's profile. """

    profile_user = UserProfile.objects.get(user=request.user)
    user_auth = get_object_or_404(User, username=request.user)

    # Render profile form with default details
    profileForm = UserProfileForm(instance=profile_user)

    # Render redeem subscription form
    redeem_sub = RedeemForm()

    if request.method == 'POST':

        form_data = {
            'default_full_name': request.POST['default_full_name'],
            'default_street_address1': request.POST['default_street_address1'],
            'default_street_address2': request.POST['default_street_address2'],
            'default_town_or_city': request.POST['default_town_or_city'],
            'default_country': request.POST['default_country']
        }

        user_profile_form = UserProfileForm(form_data, instance=profile_user)
        if user_profile_form.is_valid():
            user_profile_form.save()

            messages.success(request, "Profile details updated")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Check if user has any Sponsor Object in db
    # using user profile and email
    sponsor_exist = Sponsor.objects.filter(user_profile=profile_user,
                                           email=user_auth.email,
                                           ).exists()
    sponsor = None
    if sponsor_exist:

        # If user has Sponsor object in db, then query
        # Sponsor object using user profile and email
        sponsor = Sponsor.objects.get(user_profile=profile_user,
                                      email=user_auth.email)
    else:

        # If user has not Sponsor object in db matching
        # user profile and email, then check if user has
        # any Sponsor object in db using just email
        sponsor_exist = Sponsor.objects.filter(email=user_auth.email
                                               ).exists()

        if sponsor_exist:

            # If user has Sponsor object in db matching email
            # then query Sponsor and check if user_profile
            # field is empty
            sponsor = Sponsor.objects.get(email=user_auth.email)
            user_null = Sponsor.objects.filter(
                user_profile__isnull=True).exists()

            if user_null:

                # If user_profile field is empty, then add the
                # current user profile to user_profile field
                Sponsor.objects.filter(
                    email=user_auth.email).update(user_profile=profile_user)

    # If user has not Sponsor object in db matching
    # email, then check if user has any Sponsor
    # object in db using just user profile
    if not sponsor_exist:
        sponsor_exist = Sponsor.objects.filter(user_profile=profile_user
                                               ).exists()

        if sponsor_exist:

            # If user has Sponsor object in db matching
            # user profile, then query Sponsor
            sponsor = Sponsor.objects.get(user_profile=profile_user)

    orders = profile_user.orders.all()

    template = 'profiles/profile.html'
    context = {
        'profile': profile_user,
        'profileForm': profileForm,
        'redeem_form': redeem_sub,
        'orders': orders,
        'on_profile_page': True,
        'sponsor': sponsor
    }

    return render(request, template, context)


@login_required
def redeem_subscription(request):
    """
    Redeem any sponsorship created before the user creates
    an account
    """

    if request.method == 'POST':
        subs_id = request.POST['redeem_subs']
        last_digts_form = request.POST['last_digits']

        profile_user = UserProfile.objects.get(user=request.user)
        user_auth = get_object_or_404(User, username=request.user)

        subs_exist = Subscription.objects.filter(id=subs_id).exists()

        # Check if the subscription provided exist
        if subs_exist:
            subscription = Subscription.objects.get(id=subs_id)
            sponsor = Sponsor.objects.get(subscription=subscription)
            pay_method = sponsor.customer.default_payment_method.card
            last_digts_card = pay_method['last4']

            # Check that the last 4 digits provided by user
            # match the last 4 digits from payment card
            if last_digts_form == last_digts_card:

                # Update sponsor with the current user profile
                # and email
                Sponsor.objects.filter(
                    subscription=subscription
                    ).update(user_profile=profile_user, email=user_auth.email)

                messages.success(request, "Sponsorship Redemeed!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.error(request, "The sponsorship id or the last 4 digits\
                    does not match with any sponsorship")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            messages.error(request, "The sponsorship id or the last 4 digits\
                    does not match with any sponsorship")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def order_history(request, order_number):
    """
    A view to past confirmation for order
    """

    order = get_object_or_404(Order, order_number=order_number)

    messages.info(request, (
        f'This is a past confirmation for order number {order_number}. '
        'A confirmation email was sent on the order date.'
    ))

    template = 'checkout/checkout_success.html'
    context = {
        'order': order,
        'from_profile': True,
    }

    return render(request, template, context)
