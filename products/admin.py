from django.contrib import admin
from .models import (Product, Category,
                     Parcel)


class ProductAdmin(admin.ModelAdmin):
    """
    Sort and Displays product table in Admin interface.
    """

    list_display = ('sku',
                    'name',
                    'category',
                    'price',
                    'image')

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    """
    Sort and Displays Category table in Admin interface.
    """

    list_display = ('friendly_name', 'name')


class ParcelAdmin(admin.ModelAdmin):
    """
    Sort and Displays parcel table in Admin interface.
    """

    list_display = ('sku',
                    'name',
                    'price',
                    'image')

    ordering = ('sku',)


# Register models to construct a default form representation.
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Parcel, ParcelAdmin)
