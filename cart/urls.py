from django.urls import path
from . import views


# Base url for this app and urls for other functions in this app
urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<item_id>/<sku>/', views.add_to_cart, name='add_to_cart'),
    path('add_all/', views.add_all_cart, name='add_all_cart'),
    path('clear_cart/', views.clear_cart, name='clear_cart'),
    path('remove_from_cart/<item_id>/<sku>', views.remove_from_cart,
         name='remove_from_cart'),
    path('update_cart/<item_id>/<sku>', views.update_cart, name='update_cart'),
]
