from django.shortcuts import (render, redirect,
                              HttpResponse)
from django.http import HttpResponseRedirect
from django.contrib import messages
from products.models import (Product, Parcel)


def view_cart(request):
    """
     Render shopping cart template
    """

    template = 'cart/cart.html'

    return render(request, template)


def add_to_cart(request, item_id, sku):
    """
    Add a quantity of the specified product to the shopping cart
    """

    try:
        quantity = int(request.POST.get('quantity'))
        item_type = sku.split('_')[-1]
        redirect_url = request.POST.get('redirect_url')

        cart = request.session.get('cart', {'products': {},
                                            'parcels': {},
                                            })

        cart_products = cart['products']
        cart_parcels = cart['parcels']

        # Verify if quantity from POST request is greater than zero
        if quantity > 0:

            # Check if added item is a parcel
            if item_type == 'pc':
                parcel = Parcel.objects.get(pk=item_id)

                # If the parcel is already in the cart, then
                # increase the quantity in the cart
                if item_id in list(cart_parcels.keys()):
                    cart_parcels[item_id] += quantity
                    messages.success(request, f'Updated {parcel.name} quantity to\
                        {cart_parcels[item_id]}.')

                # If the parcel is not in the cart,
                # then add to the cart
                else:
                    cart_parcels[item_id] = quantity
                    messages.success(request, f'Added {parcel.name} to\
                        your shopping cart.')

            # If the item is not a parcel (a single product in this case)
            else:
                product = Product.objects.get(pk=item_id)

                # If the product is already in the cart, then
                # increase the quantity in the cart
                if item_id in list(cart_products.keys()):
                    cart_products[item_id] += quantity
                    messages.success(request, f'Updated {product.name} quantity to\
                        {cart_products[item_id]}.')

                # If the product is not in the cart,
                # then add to the cart
                else:
                    cart_products[item_id] = quantity
                    messages.success(request, f'Added {product.name} to\
                        your shopping cart.')
        else:
            messages.error(request, "Product Quantity need to be more than 0.")

        request.session['cart'] = cart
        return redirect(redirect_url)

    except Exception as e:
        messages.error(request, f'Error adding item to cart. {e}')
        return HttpResponse(status=500)


def add_all_cart(request):
    """
    Add a unit of all products of a specific category or sorting
    """

    try:
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

            # If any item is already in the cart,
            # then increase the quantity in the cart
            if item_id in list(cart_products.keys()):
                cart_products[item_id] += quantity

            # If none of the items is in the cart,
            # then add to the cart with quantity of 1
            else:
                cart_products[item_id] = quantity

        messages.success(request, 'Added many products to\
                    your shopping cart.')

        request.session['cart'] = cart
        return redirect(redirect_url)

    except Exception as e:
        messages.error(request, f'Error adding many items to cart. {e}')
        return HttpResponse(status=500)


def update_cart(request, item_id, sku):
    """
    Update quantity of a product in shopping cart
    """

    try:
        redirect_url = request.POST.get('redirect_url')
        quantity = int(request.POST.get('quantity'))
        item_type = sku.split('_')[-1]
        cart = request.session.get('cart', {'products': {},
                                            'parcels': {},
                                            })

        cart_products = cart['products']
        cart_parcels = cart['parcels']

        # Verify if quantity from request i greater than zero
        if quantity > 0:

            # Check if item is a parcel
            if item_type == 'pc':
                parcel = Parcel.objects.get(pk=item_id)

                # Update parcel quantity in the cart
                cart_parcels[item_id] = quantity
                messages.success(request, f'Updated {parcel.name} quantity to\
                        {cart_parcels[item_id]}.')

            # It's not a parcel (a single product in this case)
            else:
                product = Product.objects.get(pk=item_id)

                # Update product quantity in the cart
                cart_products[item_id] = quantity
                messages.success(request, f'Updated {product.name} quantity to\
                        {cart_products[item_id]}.')
        else:
            messages.error(request, "You can't update a product\
                quantity to 0.")

        request.session['cart'] = cart
        return redirect(redirect_url)

    except Exception as e:
        messages.error(request, f'Error updating cart. {e}')
        return HttpResponse(status=500)


def remove_from_cart(request, item_id, sku):
    """
    Remove a product from shopping cart
    """

    try:
        item_type = sku.split('_')[-1]
        cart = request.session.get('cart', {'products': {},
                                            'parcels': {},
                                            })

        cart_products = cart['products']
        cart_parcels = cart['parcels']

        # Check if item is a parcel
        if item_type == 'pc':
            parcel = Parcel.objects.get(pk=item_id)

            # Remove the parcel from cart
            cart_parcels.pop(item_id)
            messages.success(request, f'Removed {parcel.name} from\
                    your shopping cart.')

        # It's not a parcel (a single product in this case)
        else:
            product = Product.objects.get(pk=item_id)

            # Remove product from cart
            cart_products.pop(item_id)
            messages.success(request, f'Removed {product.name} from\
                    your shopping cart.')

        request.session['cart'] = cart
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        messages.error(request, f'Error removing item from cart. {e}')
        return HttpResponse(status=500)


def clear_cart(request):
    """
    Remove all products from shopping cart
    """

    try:
        if 'cart' in request.session:

            # Delete cart session (remove all items from cart)
            del request.session['cart']
            messages.success(request, 'Removed all products from\
                    your shopping cart.')
        else:
            messages.error(request, 'There is no product\
                    in your shopping cart.')

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    except Exception as e:
        messages.error(request, f'Error removing all items from cart. {e}')
        return HttpResponse(status=500)
