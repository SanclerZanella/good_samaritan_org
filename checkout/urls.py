from django.urls import path
from . import views
from .webhooks import webhook


# Base url for this app and urls for other functions in this app
urlpatterns = [
    path('', views.checkout, name='checkout'),
    path('render_pdf/<order_number>', views.render_pdf, name="render_pdf"),
    path('checkout_success/<order_number>', views.checkout_success,
         name='checkout_success'),
    path('wh/', webhook, name='webhook'),
]
