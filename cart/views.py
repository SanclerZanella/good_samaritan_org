from django.shortcuts import (render, redirect,
                              reverse, HttpResponse,
                              get_object_or_404)
from django.http import HttpResponseRedirect
from django.contrib import messages
from products.models import Product, Parcel


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


def add_all_cart(request):
    """ Add a unit of all products of a specific category or sorting """

    quantity = 1
    redirect_url = request.POST.get('redirect_url')
    items_list = request.POST.get('items_list')
    id_list = items_list.replace('[', " ").replace(']', ' ')\
        .replace(',', ' ').split()

    cart = request.session.get('cart', {'products': {},
                                        'parcels': {},
                                        })

    cart_products = cart['products']

    for item_id in id_list:

        if item_id in list(cart_products.keys()):
            cart_products[item_id] += quantity
        else:
            cart_products[item_id] = quantity

    request.session['cart'] = cart
    return redirect(redirect_url)


def update_cart(request, item_id, sku):

    redirect_url = request.POST.get('redirect_url')
    quantity = int(request.POST.get('quantity'))
    item_type = sku.split('_')[-1]
    cart = request.session.get('cart', {'products': {},
                                        'parcels': {},
                                        })

    cart_products = cart['products']
    cart_parcels = cart['parcels']

    print('HERE!!!')
    print(cart_products[item_id])

    if item_type == 'pc':
        cart_parcels[item_id] = quantity
    else:
        cart_products[item_id] = quantity

    request.session['cart'] = cart

    return redirect(redirect_url)


def remove_from_cart(request, item_id, sku):

    # redirect_url = request.POST.get('redirect_url')
    item_type = sku.split('_')[-1]
    cart = request.session.get('cart', {'products': {},
                                        'parcels': {},
                                        })

    cart_products = cart['products']
    cart_parcels = cart['parcels']

    if item_type == 'pc':
        cart_parcels.pop(item_id)
    else:
        cart_products.pop(item_id)

    request.session['cart'] = cart
    return render(request, 'cart/cart.html')


def clear_cart(request):
    if 'cart' in request.session:
        del request.session['cart']

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
