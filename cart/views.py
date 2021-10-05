from django.shortcuts import (render, redirect,
                              reverse, HttpResponse,
                              get_object_or_404)
from django.http import HttpResponseRedirect
from django.contrib import messages
from products.models import Product


def view_cart(request):
    template = 'cart/cart.html'
    context = {
    }

    return render(request, template, context)


def add_to_cart(request, item_id, sku):
    """ Add a quantity of the specified product to the shopping cart """

    quantity = int(request.POST.get('quantity'))
    item_type = sku.split('_')[-1]
    redirect_url = request.POST.get('redirect_url')

    cart = request.session.get('cart', {'products': {},
                                        'parcels': {},
                                        })

    cart_products = cart['products']
    cart_parcels = cart['parcels']

    if item_type == 'pc':
        if item_id in list(cart_parcels.keys()):
            cart_parcels[item_id] += quantity
        else:
            cart_parcels[item_id] = quantity
    else:
        if item_id in list(cart_products.keys()):
            cart_products[item_id] += quantity
        else:
            cart_products[item_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)


def add_all_cart(request, all_items):
    """ Add a unit of all products of a specific category or sorting """

    quantity = 1
    redirect_url = request.POST.get('redirect_url')

    cart = request.session.get('cart', {'products': {},
                                        'parcels': {},
                                        })

    cart_products = cart['products']

    for n_id in range(int(all_items)):
        item_id = n_id + 1

        if item_id in list(cart_products.keys()):
            cart_products[item_id] += quantity
        else:
            cart_products[item_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)


def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))