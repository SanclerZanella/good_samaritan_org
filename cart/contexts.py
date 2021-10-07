from django.shortcuts import get_object_or_404
from products.models import Product, Parcel


def cart_contents(request):
    """
    Products info in the cart available to all pages
    """

    cart_items = []
    total = 0
    product_count = 0
    cart = request.session.get('cart', {'products': {},
                                        'parcels': {},
                                        })

    cart_products = cart['products']
    cart_parcels = cart['parcels']

    if cart_products.items():
        for item_id, item_qty in cart_products.items():
            if isinstance(item_qty, int):
                product = get_object_or_404(Product, pk=item_id)
                total += item_qty * product.price
                product_count += item_qty
                cart_items.append({
                    'item_id': item_id,
                    'quantity': item_qty,
                    'product': product
                })

    if cart_parcels.items():
        for item_id, item_qty in cart_parcels.items():
            if isinstance(item_qty, int):
                parcel = get_object_or_404(Parcel, pk=item_id)
                total += item_qty * parcel.price
                product_count += item_qty
                cart_items.append({
                    'item_id': item_id,
                    'quantity': item_qty,
                    'product': parcel
                })

    context = {
        'cart_items': cart_items,
        'grand_total': total,
        'product_count': product_count
    }

    return context
