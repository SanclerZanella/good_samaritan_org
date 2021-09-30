from django.contrib import admin
from .models import (Product, Category,
                     Parcel)


class ProductAdmin(admin.ModelAdmin):
    list_display = ('sku',
                    'name',
                    'category',
                    'price',
                    'image')

    ordering = ('sku',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('friendly_name', 'name')


class ParcelAdmin(admin.ModelAdmin):
    list_display = ('sku',
                    'name',
                    'price',
                    'image')

    ordering = ('sku',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Parcel, ParcelAdmin)
