from django.urls import path
from . import views


# Base url for this app and urls for other functions in this app
urlpatterns = [
    path('', views.all_products, name='products'),
    path('parcels/', views.parcels, name='parcels'),
]
