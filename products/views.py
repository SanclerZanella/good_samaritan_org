from django.shortcuts import render
from django.conf import settings
from .models import (Product, Category,
                     Parcel)


def all_products(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    query = None
    current_category = None
    sort = None
    direction = None

    current_sorting = f'{sort}_{direction}'

    template = 'products/products.html'
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
        'products': products,
        'categories': categories,
        'current_category': current_category,
        'search_term': query,
        'current_sorting': current_sorting,
    }

    return render(request, template, context)
