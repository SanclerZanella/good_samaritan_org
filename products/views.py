from django.shortcuts import render
from django.conf import settings
from .models import (Product, Category,
                     Parcel)
from django.core.paginator import (Paginator, EmptyPage,
                                   PageNotAnInteger)


def all_products(request):
    all_products = Product.objects.all()
    all_products_len = len(all_products)
    categories = Category.objects.all()
    query = None
    current_category = None
    sort = None
    direction = None

    page = request.GET.get('page', 1)
    paginator = Paginator(all_products, 20)

    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    current_sorting = f'{sort}_{direction}'

    template = 'products/products.html'
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'search_term': query,
        'current_sorting': current_sorting,
        'all_products_len': all_products_len,
    }

    return render(request, template, context)
