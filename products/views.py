from django.shortcuts import (render, redirect,
                              reverse, get_object_or_404,
                              HttpResponse)
from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.db.models import Q, Sum
from django.db.models.functions import Lower
from django.contrib.auth.decorators import user_passes_test
from .models import (Product, Category,
                     Parcel)
from checkout.models import Sponsor
from djstripe.models import Subscription, Customer, PaymentMethod
from djstripe.models import Product as Sponsorship
import djstripe.models
import djstripe.settings
from .forms import ProductForm, ParcelForm
from checkout.forms import SponsorForm
from django.core.paginator import (Paginator, EmptyPage,
                                   PageNotAnInteger)
from .utils import get_id_data
import stripe


def all_products(request):
    """
    A view to show all products, including sorting and search queries
    """

    products_ex = Product.objects.all().exists()
    if products_ex:
        all_products = Product.objects.all()
    else:
        messages.error(request,
                       "There are no products")
        return redirect(reverse('home'))

    all_products_len = len(all_products)
    sum_price = all_products.aggregate(Sum('price'))
    total_price = round(sum_price['price__sum'], 2)
    all_items = get_id_data(all_products)
    categories = Category.objects.all()
    query = None
    current_category = None
    sort = None
    direction = None
    most_n = None

    if request.GET:

        # Query products by sorting
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey
            if sortkey == 'name':
                sortkey = 'lower_name'
                all_products = all_products.annotate(lower_name=Lower('name'))
                all_products_len = len(all_products)
                sum_price = all_products.aggregate(Sum('price'))
                total_price = round(sum_price['price__sum'], 2)
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
            sum_price = all_products.aggregate(Sum('price'))
            total_price = round(sum_price['price__sum'], 2)
            all_items = get_id_data(all_products)
            most_n = None

        # Query products by category
        if 'category' in request.GET:
            category = request.GET['category'].split(',')
            all_products = all_products.filter(category__name__in=category)
            all_products_len = len(all_products)
            sum_price = all_products.aggregate(Sum('price'))
            total_price = round(sum_price['price__sum'], 2)
            all_items = get_id_data(all_products)
            ctg = get_object_or_404(Category, name=request.GET['category'])
            current_category = ctg.friendly_name
            most_n = None

        # Query products by searching
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request,
                               "You didn't enter any search criteria!")
                return redirect(reverse('products'))

            qr1 = Q(name__icontains=query)
            qr2 = Q(description__icontains=query)
            queries = qr1 | qr2
            all_products = all_products.filter(queries)
            all_products_len = len(all_products)
            sum_price = all_products.aggregate(Sum('price'))
            total_price = round(sum_price['price__sum'], 2)
            all_items = get_id_data(all_products)
            most_n = None

        # Query products by most-needed status
        if 'urgent' in request.GET:
            m_needed_ex = all_products.filter(m_needed=True).exists()

            if m_needed_ex:
                all_products = all_products.filter(m_needed=True)
                all_products_len = len(all_products)
                sum_price = all_products.aggregate(Sum('price'))
                total_price = round(sum_price['price__sum'], 2)
                all_items = get_id_data(all_products)
                current_category = None
                most_n = True
            else:
                all_products = Product.objects.all()
                all_products_len = len(all_products)
                sum_price = all_products.aggregate(Sum('price'))
                total_price = round(sum_price['price__sum'], 2)
                all_items = get_id_data(all_products)
                current_category = None
                most_n = False

    current_sorting = f'{sort}_{direction}'
    page = request.GET.get('page', 1)
    paginator = Paginator(all_products, 20)

    # Create pagination and define number of products per page
    # use pagination to infinite scroll
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    template = 'products/products.html'
    context = {
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'search_term': query,
        'current_sorting': current_sorting,
        'all_products_len': all_products_len,
        'total_price': total_price,
        'all_items': all_items,
        'most_n': most_n,
    }

    return render(request, template, context)


def parcels(request):
    """
    A view to show all parcel
    """

    products_ex = Product.objects.all().exists()
    parcels_ex = Parcel.objects.all().exists()
    if products_ex and parcels_ex:
        parcels = Parcel.objects.all()
    else:
        messages.error(request,
                       "There are no parcels")
        return redirect(reverse('home'))

    parcels = Parcel.objects.all()
    parcel = get_object_or_404(Parcel, pk=1)

    list_items = parcel.items
    items_ids = list_items.split(',')
    items_in_parcel = list()

    # Items in the chosen parcel
    for item in items_ids:
        item_id = int(item)
        items_in_parcel.append(Product.objects.get(pk=item_id))

    if request.GET:
        if 'parcel' in request.GET:
            parcel_param = request.GET['parcel'].split('_')
            parcel_id = int(parcel_param[-1])
            parcel = get_object_or_404(Parcel, pk=parcel_id)

            list_items = parcel.items
            items_ids = list_items.split(',')
            items_in_parcel = list()

            # Items in the chosen parcel
            for item in items_ids:
                item_id = int(item)
                items_in_parcel.append(Product.objects.get(pk=item_id))

    template = 'products/parcels.html'
    context = {
        'parcels': parcels,
        'parcel': parcel,
        'items_in_parcel': items_in_parcel,
    }

    return render(request, template, context)


def product_details(request, product_id):
    """
    A view to show product details
    """

    product = get_object_or_404(Product, pk=product_id)

    template = 'products/product_details.html'
    context = {
        'product': product,
    }

    return render(request, template, context)


def sponsorship(request):
    """
    A view to render the sponsorship page
    """

    sponsor_op = Sponsorship.objects.all()
    sponsor_ex = Sponsorship.objects.filter(id='prod_KTO0rZ3DSbX6cu').exists()

    if sponsor_ex:
        sponsor = get_object_or_404(Sponsorship, id='prod_KTO0rZ3DSbX6cu')
    else:
        stripe.api_key = settings.STRIPE_SECRET_KEY

        # sponsor a child

        # Retrieve Product
        stripe_product_c = stripe.Product.retrieve("prod_KTO0rZ3DSbX6cu")

        if stripe_product_c:
            djstripe.models.Product.sync_from_stripe_data(stripe_product_c)

            # Retrieve Plan
            stripe_plan_c = stripe.Plan.retrieve("price_1JoREqK073rHrzv3AiYRMd6M")
            djstripe.models.Plan.sync_from_stripe_data(stripe_plan_c)

            # Retrieve Price
            stripe_price_c = stripe.Price.retrieve("price_1JoREqK073rHrzv3AiYRMd6M")
            djstripe.models.Price.sync_from_stripe_data(stripe_price_c)

            sponsor = get_object_or_404(Sponsorship, id='prod_KTO0rZ3DSbX6cu')

            # sponsor a widow

            # Retrieve Product
            stripe_product_w = stripe.Product.retrieve("prod_KTO2NqA3YSYuwN")
            djstripe.models.Product.sync_from_stripe_data(stripe_product_w)

            # Retrieve Plan
            stripe_plan_w = stripe.Plan.retrieve("price_1JoRGhK073rHrzv3gyPNKRFX")
            djstripe.models.Plan.sync_from_stripe_data(stripe_plan_w)

            # Retrieve Price
            stripe_price_w = stripe.Price.retrieve("price_1JoRGhK073rHrzv3gyPNKRFX")
            djstripe.models.Price.sync_from_stripe_data(stripe_price_w)

            # sponsor an elderly
            stripe_product_e = stripe.Product.retrieve("prod_KTO3PepAZNLNtl")
            djstripe.models.Product.sync_from_stripe_data(stripe_product_e)

            # Retrieve Plan
            stripe_plan_e = stripe.Plan.retrieve("price_1JoRHbK073rHrzv3ATAy15nG")
            djstripe.models.Plan.sync_from_stripe_data(stripe_plan_e)

            # Retrieve Price
            stripe_price_e = stripe.Price.retrieve("price_1JoRHbK073rHrzv3ATAy15nG")
            djstripe.models.Price.sync_from_stripe_data(stripe_price_e)
        else:
            messages.error(request,
                           "There are no sponsorships")
        return redirect(reverse('home'))

    if request.GET:
        if 'sponsor' in request.GET:
            sponsor_param = request.GET['sponsor'].split('-')
            sponsor_id = sponsor_param[-1]
            sponsor = get_object_or_404(Sponsorship, id=sponsor_id)

    context = {
        'sponsor_op': sponsor_op,
        'sponsor': sponsor,
    }

    template = 'products/sponsorship.html'
    return render(request, template, context)


@user_passes_test(lambda u: u.is_superuser)
def product_mangement(request):
    """
    A view to render the product management dashboard
    """

    products_ex = Product.objects.all().exists()
    if products_ex:
        all_products = Product.objects.all()
    else:
        messages.error(request,
                       "There are no products")
        return redirect(reverse('home'))

    form = ProductForm()
    all_parcels = None
    all_products_len = len(all_products)
    categories = Category.objects.all()
    query = None
    sort = None
    direction = None
    parcel_param = None

    # Query products by sorting
    if 'sort' in request.GET:
        sortkey = request.GET['sort']
        sort = sortkey
        if sort == 'name':
            sortkey = 'lower_name'
            all_products = all_products.annotate(lower_name=Lower('name'))
            all_products_len = len(all_products)
        if sort == 'category':
            sortkey = 'category__name'
        if 'direction' in request.GET:
            direction = request.GET['direction']
            if direction == 'desc':
                sortkey = f'-{sortkey}'
        all_products = all_products.order_by(sortkey)
        all_products_len = len(all_products)

    # Query products by category
    if 'category' in request.GET:
        category = request.GET['category'].split(',')
        all_products = all_products.filter(category__name__in=category)
        all_products_len = len(all_products)

    # Query products by searching
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

    # Query products by most-needed status
    if 'urgent' in request.GET:
        all_products = all_products.filter(m_needed=True)
        all_products_len = len(all_products)

    # Query products by parcel category
    if 'parcel' in request.GET:
        all_parcels = Parcel.objects.all()
        all_products_len = len(all_parcels)
        parcel_param = True

    template = 'products/product_management.html'
    context = {
        'categories': categories,
        'products': all_products,
        'parcels': all_parcels,
        'all_products_len': all_products_len,
        'parcel_param': parcel_param,
        'form': form,
    }

    return render(request, template, context)


@user_passes_test(lambda u: u.is_superuser)
def add_product(request):
    """ Add a new product to the shop """

    # Restric functionality to superuser
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site staff can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':

        # New product form
        form = ProductForm(request.POST, request.FILES)

        # Add new product to db
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            return redirect(reverse('product_details', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product.\
                Please ensure the form is valid.')

    return redirect(reverse('product_management'))


@user_passes_test(lambda u: u.is_superuser)
def edit_product(request, product_id, product_sku):
    """ Edit a product in the shop """

    # Restric functionality to superuser
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store managers can do that.')
        return redirect(reverse('products'))

    item_type = product_sku.split('_')[-1]
    products = Product.objects.all()

    # Verify if the item is a parcel
    if item_type == 'pc':
        product = get_object_or_404(Parcel, pk=product_id)
        list_items = product.items
        items_ids = list_items.split(',')
        items_in_parcel = list()

        # Append all parcel items to items_in_parcel list
        for item in items_ids:
            item_id = int(item)
            items_in_parcel.append(Product.objects.get(pk=item_id))

    else:
        product = get_object_or_404(Product, pk=product_id)
        items_in_parcel = None

    if request.method == 'POST':

        # Verify if the item is a parcel
        if item_type == 'pc':

            # Render form to edit a parcel
            form = ParcelForm(request.POST, request.FILES, instance=product)

        # It's not a parcel (a single product in this case)
        else:

            # Render form to edit a product
            form = ProductForm(request.POST, request.FILES, instance=product)

        # Update parcel or product on db
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_management'))
        else:
            messages.error(request, 'Failed to update product.\
                Please ensure the form is valid.')
    else:
        if item_type == 'pc':

            # Render form to edit a parcel
            form = ParcelForm(instance=product)
        else:

            # Render form to edit a product
            form = ProductForm(instance=product)

        messages.info(request, f'You are editing {product.name}')

    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
        'products': products,
        'items_in_parcel': items_in_parcel,
    }

    return render(request, template, context)


@user_passes_test(lambda u: u.is_superuser)
def delete_product(request, product_id):
    """ Delete a product from the shop """

    # Restric functionality to superuser
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site staff can do that.')
        return redirect(reverse('home'))

    # Delete chosen product from db
    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')

    return redirect(reverse('product_management'))


@user_passes_test(lambda u: u.is_superuser)
def delete_product_parcel(request, parcel_id, product_id):
    """ Delete a product from the parcel items """

    # Restric functionality to superuser
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site staff can do that.')
        return redirect(reverse('home'))

    parcel = get_object_or_404(Parcel, pk=parcel_id)
    list_items = parcel.items
    items_ids = list_items.split(',')
    items_in_parcel = list()

    # Append products from parcel to items_in_parcel
    for item in items_ids:
        item_id = int(item)
        items_in_parcel.append(Product.objects.get(pk=item_id).id)

    # Remove product from parcel
    if int(product_id) in items_in_parcel:
        items_in_parcel.remove(int(product_id))
        list_string = ",".join(str(id) for id in items_in_parcel)
        Parcel.objects.filter(pk=parcel.id).update(items=list_string)

    messages.success(request, 'Product deleted from parcel!')
    return redirect(reverse('edit_product', args=[parcel.id, parcel.sku]))


@user_passes_test(lambda u: u.is_superuser)
def add_product_parcel(request):
    """ Add a product to the parcel items """

    # Restric functionality to superuser
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site staff can do that.')
        return redirect(reverse('home'))

    parcel_id = None
    product_id = None

    # Get parcel id
    if 'parcel_id' in request.POST:
        parcel_id = request.POST['parcel_id']
    else:
        messages.error(request, 'You have select a product\
            before add to the parcel')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    # Get product id
    if 'product_id' in request.POST:
        product_id = request.POST['product_id']

    parcel = get_object_or_404(Parcel, pk=parcel_id)
    list_items = parcel.items
    items_ids = list_items.split(',')
    items_in_parcel = list()
    product_id_list = list(map(int, product_id.split(',')))

    # Append products from parcel to items_in_parcel
    for item in items_ids:
        item_id = int(item)
        items_in_parcel.append(Product.objects.get(pk=item_id).id)

    # Add product to parcel
    items_in_parcel.extend(product_id_list)
    new_products_list = sorted(list(set(items_in_parcel)))
    new_products = ",".join(map(str, new_products_list))
    Parcel.objects.filter(pk=parcel_id).update(items=new_products)

    messages.success(request, 'Product added to parcel!')
    return HttpResponse(status=200)


def finish_sponsorship_form(request):
    """
    A view to render the finish sponsorship form
    """

    form = SponsorForm()
    subscription = None
    sponsor = None
    subs_query = None

    if request.method == 'POST':
        try:
            subs_id = request.POST['subscription_id'].strip()
            full_name = request.POST['full_name'].strip()
            email = request.POST['email'].strip()
            address1 = request.POST['street_address1'].strip()
            address2 = request.POST['street_address2'].strip()
            city = request.POST['town_or_city'].strip()
            country = request.POST['country'].strip()

            subs_exist = Subscription.objects.filter(id=subs_id).exists()

            sponsor_exist = Sponsor.objects.filter(full_name=full_name,
                                                   email=email,
                                                   street_address1=address1,
                                                   street_address2=address2,
                                                   town_or_city=city,
                                                   country=country
                                                   ).exists()

            # Check if sponsorship exists
            if subs_exist and sponsor_exist:
                subscription = Subscription.objects.get(id=subs_id)
                sponsor = Sponsor.objects.get(full_name=full_name,
                                              email=email,
                                              street_address1=address1,
                                              street_address2=address2,
                                              town_or_city=city,
                                              country=country
                                              )

                # Check if sponsor and subscription are related
                if sponsor.subscription == subscription:
                    subs_query = True
                else:
                    subs_query = None
                    subscription = None
                    sponsor = None
                    messages.error(request, "We can't find the subscription with this\
                        subscription id. Are you providing the\
                            right subscription id?")

                    return HttpResponseRedirect(
                        request.META.get('HTTP_REFERER'))

            else:
                subs_query = None
                subscription = None
                sponsor = None
                messages.error(request, "We can't find the subscription with this\
                    subscription id. Are you providing the right subscription\
                        id?")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        except Exception:
            subs_query = None
            subscription = None
            sponsor = None
            messages.error(request, "We can't find the subscription with this\
                subscription id. Are you providing the right subscription id?")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    context = {
        'form': form,
        'subs_query': subs_query,
        'subscription': subscription,
        'sponsor': sponsor,

    }

    template = 'products/finish_sponsorship.html'
    return render(request, template, context)


def finish_sponsorship(request, customer_id):
    """
    Delete subscription from database and stripe
    """

    # Delete Sponsor and Customer object
    customer = Customer.objects.get(id=customer_id)
    Sponsor.objects.filter(customer=customer).delete()
    PaymentMethod.objects.filter(
        id=customer.default_payment_method.id).delete()
    Customer.objects.filter(id=customer_id).delete()

    # Delete Customer from stripe
    stripe.api_key = settings.STRIPE_SECRET_KEY
    stripe.Customer.delete(customer_id)

    messages.success(request, "Sponsorship Finished")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
