from django.urls import path
from . import views


# Base url for this app and urls for other functions in this app
urlpatterns = [
    path('', views.profile, name='profile'),
    path('order_history/<order_number>/', views.order_history,
         name='order_history'),
    path('redeem_subscription/', views.redeem_subscription,
         name='redeem_subscription'),
]
