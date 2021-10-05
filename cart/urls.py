from django.urls import path
from . import views


# Base url for this app and urls for other functions in this app
urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<item_id>/<sku>', views.add_to_cart, name='add_to_cart'),
    path('add_all/<all_items>', views.add_all_cart, name='add_all_cart'),
]
