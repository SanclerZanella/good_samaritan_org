from django.shortcuts import (render, get_object_or_404,
                              redirect, reverse)
from .models import UserProfile
from .forms import UserProfileForm
from django.db.models import Q
from django.db.models.functions import Lower
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from checkout.models import Order
from products.models import (Product, Parcel, Category)
from products.utils import get_id_data


@login_required
def profile(request):
    """ Display the user's profile. """
    profile_user = get_object_or_404(UserProfile, user=request.user)

    profileForm = UserProfileForm(instance=profile_user)
    orders = profile_user.orders.all()

    template = 'profiles/profile.html'
    context = {
        'profile': profile_user,
        'profileForm': profileForm,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)


def order_history(request, order_number):
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
