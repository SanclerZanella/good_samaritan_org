from django.contrib import admin
from .models import Order, OrderLineItem, Sponsor


class OrderLineItemAdminInline(admin.TabularInline):
    """
    Sort and Displays products table in an Order
    object in Admin interface.
    """

    model = OrderLineItem
    readonly_fields = ('lineitem_total',)


class OrderAdmin(admin.ModelAdmin):
    """
    Sort and Displays Order table in Admin interface.
    """

    inlines = (OrderLineItemAdminInline,)

    readonly_fields = ('order_number', 'date',
                       'grand_total', 'original_cart',
                       'stripe_pid')

    fields = ('order_number', 'user_profile', 'date', 'full_name',
              'email', 'country', 'town_or_city', 'street_address1',
              'street_address2', 'grand_total', 'original_cart',
              'stripe_pid')

    list_display = ('order_number', 'date', 'full_name',
                    'grand_total',)

    ordering = ('-date',)


class SponsorAdmin(admin.ModelAdmin):
    """
    Sort and Displays Sponsor table in Admin interface.
    """

    readonly_fields = ('customer', 'subscription', 'user_profile', 'date',
                       'grand_total')

    fields = ('customer', 'subscription', 'user_profile', 'date', 'full_name',
              'email', 'country', 'town_or_city', 'street_address1',
              'street_address2', 'grand_total')

    list_display = ('customer', 'subscription', 'date', 'full_name',
                    'grand_total',)

    ordering = ('-date',)


# Register Order and Sponsor model
admin.site.register(Order, OrderAdmin)
admin.site.register(Sponsor, SponsorAdmin)
