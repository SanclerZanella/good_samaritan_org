from django.shortcuts import (render, redirect,
                              reverse, get_object_or_404,
                              HttpResponse)
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.db.models import Q, Sum
from django.db.models.functions import Lower
from django.contrib.auth.decorators import user_passes_test
from .models import (Product, Category,
                     Parcel)
from djstripe.models import Product as Sponsorship
from .forms import ProductForm, ParcelForm
from django.core.paginator import (Paginator, EmptyPage,
                                   PageNotAnInteger)
from .utils import get_id_data


def all_products(request):
    """
    A view to show all products, including sorting and search queries
    """

    all_products = Product.objects.all()
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

        if 'urgent' in request.GET:
            all_products = all_products.filter(m_needed=True)
            all_products_len = len(all_products)
            sum_price = all_products.aggregate(Sum('price'))
            total_price = round(sum_price['price__sum'], 2)
            all_items = get_id_data(all_products)
            current_category = None
            most_n = True

    current_sorting = f'{sort}_{direction}'
    page = request.GET.get('page', 1)
    paginator = Paginator(all_products, 20)

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

    parcels = Parcel.objects.all()
    parcel = get_object_or_404(Parcel, pk=1)

    list_items = parcel.items
    items_ids = list_items.split(',')
    items_in_parcel = list()

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

    sponsor_op = Sponsorship.objects.all()
    sponsor = get_object_or_404(Sponsorship, id='prod_KTO0rZ3DSbX6cu')

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

    form = ProductForm()
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
            if sortkey == 'category':
                sortkey = 'category__name'
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'desc':
                    sortkey = f'-{sortkey}'
            all_products = all_products.order_by(sortkey)
            all_products_len = len(all_products)

        if 'category' in request.GET:
            category = request.GET['category'].split(',')
            all_products = all_products.filter(category__name__in=category)
            all_products_len = len(all_products)

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

        if 'urgent' in request.GET:
            all_products = all_products.filter(m_needed=True)
            all_products_len = len(all_products)
            most_n = True

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
    """ Add a product to the shop """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site staff can do that.')
        return redirect(reverse('home'))

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
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
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store managers can do that.')
        return redirect(reverse('products'))

    item_type = product_sku.split('_')[-1]
    products = Product.objects.all()

    if item_type == 'pc':
        product = get_object_or_404(Parcel, pk=product_id)
        list_items = product.items
        items_ids = list_items.split(',')
        items_in_parcel = list()

        for item in items_ids:
            item_id = int(item)
            items_in_parcel.append(Product.objects.get(pk=item_id))

    else:
        product = get_object_or_404(Product, pk=product_id)
        items_in_parcel = None

    if request.method == 'POST':
        if item_type == 'pc':
            form = ParcelForm(request.POST, request.FILES, instance=product)
        else:
            form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')
            return redirect(reverse('product_management'))
        else:
            messages.error(request, 'Failed to update product.\
                Please ensure the form is valid.')
    else:
        if item_type == 'pc':
            form = ParcelForm(instance=product)
        else:
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
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site staff can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, id=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('product_management'))


@user_passes_test(lambda u: u.is_superuser)
def delete_product_parcel(request, parcel_id, product_id):
    """ Delete a product from the parcel items """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site staff can do that.')
        return redirect(reverse('home'))

    parcel = get_object_or_404(Parcel, pk=parcel_id)
    list_items = parcel.items
    items_ids = list_items.split(',')
    items_in_parcel = list()

    for item in items_ids:
        item_id = int(item)
        items_in_parcel.append(Product.objects.get(pk=item_id).id)

    if int(product_id) in items_in_parcel:
        items_in_parcel.remove(int(product_id))
        list_string = ",".join(str(id) for id in items_in_parcel)
        Parcel.objects.filter(pk=parcel.id).update(items=list_string)

    messages.success(request, 'Product deleted from parcel!')
    return redirect(reverse('edit_product', args=[parcel.id, parcel.sku]))


@user_passes_test(lambda u: u.is_superuser)
def add_product_parcel(request):
    """ Add a product to the parcel items """
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only site staff can do that.')
        return redirect(reverse('home'))

    parcel_id = None
    product_id = None

    if 'parcel_id' in request.POST:
        parcel_id = request.POST['parcel_id']
    else:
        messages.error(request, 'You have select a product\
            before add to the parcel')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    if 'product_id' in request.POST:
        product_id = request.POST['product_id']

    parcel = get_object_or_404(Parcel, pk=parcel_id)
    list_items = parcel.items
    items_ids = list_items.split(',')
    items_in_parcel = list()
    product_id_list = list(map(int, product_id.split(',')))

    for item in items_ids:
        item_id = int(item)
        items_in_parcel.append(Product.objects.get(pk=item_id).id)

    items_in_parcel.extend(product_id_list)
    new_products_list = sorted(list(set(items_in_parcel)))
    new_products = ",".join(map(str, new_products_list))

    Parcel.objects.filter(pk=parcel_id).update(items=new_products)

    messages.success(request, 'Product added to parcel!')
    return HttpResponse(status=200)
