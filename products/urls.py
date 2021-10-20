from django.urls import path
from . import views


# Base url for this app and urls for other functions in this app
urlpatterns = [
    path('', views.all_products, name='products'),
    path('parcels/', views.parcels, name='parcels'),
    path('product_management/', views.product_mangement,
         name='product_management'),
    path('<int:product_id>/', views.product_details, name='product_details'),
    path('add_product/', views.add_product, name='add_product'),
    path('delete_product/<product_id>/', views.delete_product,
         name='delete_product'),
]
