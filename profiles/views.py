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
    all_products = Product.objects.all()
    all_parcels = None
    all_products_len = len(all_products)
    categories = Category.objects.all()
    query = None
    sort = None
    direction = None
    most_n = None
    parcel_param = None

    if request.method == 'POST':
        profileForm = UserProfileForm(request.POST, instance=profile_user)
        if profileForm.is_valid():
            profileForm.save()
            messages.success(request, 'Profile updated successfully')
    else:
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                all_products = all_products.annotate(lower_name=Lower('name'))
                all_products_len = len(all_products)
                all_items = get_id_data(all_products)
                most_n = None
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            all_products = all_products.order_by(sortkey)
            all_products_len = len(all_products)
            all_items = get_id_data(all_products)
            most_n = None

        if 'category' in request.GET:
            category = request.GET['category'].split(',')
            all_products = all_products.filter(category__name__in=category)
            all_products_len = len(all_products)
            all_items = get_id_data(all_products)
            ctg = get_object_or_404(Category, name=request.GET['category'])
            current_category = ctg.friendly_name
            most_n = None

        if 'q-mg' in request.GET:
            query = request.GET['q-mg']
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse('profile'))

            qr1 = Q(name__icontains=query)
            qr2 = Q(description__icontains=query)
            queries = qr1 | qr2
            all_products = all_products.filter(queries)
            all_products_len = len(all_products)
            all_items = get_id_data(all_products)
            most_n = None

        if 'urgent' in request.GET:
            all_products = all_products.filter(m_needed=True)
            all_products_len = len(all_products)
            all_items = get_id_data(all_products)
            current_category = None
            most_n = True

        if 'parcel' in request.GET:
            all_parcels = Parcel.objects.all()
            all_products_len = len(all_parcels)
            all_items = get_id_data(all_parcels)
            current_category = None
            most_n = None
            parcel_param = True

    current_sorting = f'{sort}_{direction}'

    profileForm = UserProfileForm(instance=profile_user)
    orders = profile_user.orders.all()

    template = 'profiles/profile.html'
    context = {
        'profile': profile_user,
        'profileForm': profileForm,
        'orders': orders,
        'categories': categories,
        'products': all_products,
        'parcels': all_parcels,
        'all_products_len': all_products_len,
        'on_profile_page': True,
        'parcel_param': parcel_param,
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
