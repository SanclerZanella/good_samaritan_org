from django.urls import path
from . import views


# Base url for this app and urls for other functions in this app
urlpatterns = [
    path('', views.all_products, name='products'),
    path('parcels/', views.parcels, name='parcels'),
    path('product_management/', views.product_mangement,
         name='product_management'),
    path('sponsorship/', views.sponsorship, name='sponsorship'),
    path('<int:product_id>/', views.product_details, name='product_details'),
    path('add_product/', views.add_product, name='add_product'),
    path('finish_sponsorship_form/', views.finish_sponsorship_form,
         name='finish_sponsorship_form'),
    path('finish_sponsorship/<customer_id>/', views.finish_sponsorship,
         name='finish_sponsorship'),
    path('edit_product/<product_id>/<product_sku>', views.edit_product,
         name='edit_product'),
    path('delete_product_parcel/<parcel_id>/<product_id>',
         views.delete_product_parcel, name='delete_product_parcel'),
    path('add_product_parcel/',
         views.add_product_parcel, name='add_product_parcel'),
    path('delete_product/<product_id>/', views.delete_product,
         name='delete_product')
]
