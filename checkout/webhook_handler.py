from django.http import HttpResponse
from django.core.mail import send_mail
from django.template.loader import render_to_string
from datetime import datetime
from django.conf import settings
from .models import Order, OrderLineItem, Sponsor
from products.models import Product
from profiles.models import UserProfile
from djstripe.models import Subscription, Customer
import json
import time


class StripeWH_Handler:
    """Handle Stripe webhooks"""

    def __init__(self, request):
        self.request = request

    def _send_confirmation_email(self, order):
        """Send the user a confirmation email"""
        cust_email = order.email
        subject = render_to_string(
            'checkout/confirmation_emails/confirmation_email_subject.txt',
            {'order': order})
        body = render_to_string(
            'checkout/confirmation_emails/confirmation_email_body.txt',
            {'order': order, 'contact_email': settings.DEFAULT_FROM_EMAIL})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def _subscription_confirmation_email(self, sponsor):
        """Send the user a confirmation email"""
        cust_email = sponsor.email
        subs = Subscription.objects.get(customer=sponsor.customer)
        subject = render_to_string(
            'checkout/confirmation_emails/subscription_confirmation_subject.txt',
            {'sponsor': sponsor})
        body = render_to_string(
            'checkout/confirmation_emails/subscription_confirmation_body.txt',
            {'sponsor': sponsor,
             'contact_email': settings.DEFAULT_FROM_EMAIL,
             'subscription': subs})

        send_mail(
            subject,
            body,
            settings.DEFAULT_FROM_EMAIL,
            [cust_email]
        )

    def handle_event(self, event):
        """
        Handle a generic/unknown/unexpected webhook event
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_subscription_created(self, event):
        """
        Handle the customer.subscription.created webhook from Stripe
        """
        intent = event.data.object
        long_date = intent.start_date
        formated_date = datetime.fromtimestamp(long_date)
        date = formated_date.strftime('%b. %d, %Y, %H:%M %p')
        customer_id = intent.customer
        subs_id = intent.id

        customer = Customer.objects.get(id=customer_id)
        subscription = Subscription.objects.get(id=subs_id)

        metadata = intent.metadata
        pid = intent.id
        save_info = metadata.save_info
        username = intent.metadata.username

        billing_details = {
            'name': metadata.name,
            'email': metadata.email,
            'address': {
                'line1': metadata.line1,
                'line2': metadata.line2,
                'city': metadata.city,
                'country': metadata.country,
            }
        }
        address = billing_details['address']
        grand_total = round(intent.plan.amount / 100, 2)

        # Update profile information if save_info was checked
        profile = None
        if username != 'AnonymousUser':
            profile = UserProfile.objects.get(user__username=username)
            if save_info:
                profile.default_country = address['country']
                profile.default_town_or_city = address['city']
                profile.default_street_address1 = address['line1']
                profile.default_street_address2 = address['line2']
                profile.save()

        sponsor_exists = False
        attempt = 1
        while attempt <= 5:
            try:
                sponsor = Sponsor.objects.get(
                        full_name__iexact=billing_details['name'],
                        email__iexact=billing_details['email'],
                        country__iexact=address['country'],
                        town_or_city__iexact=address['city'],
                        street_address1__iexact=address['line1'],
                        street_address2__iexact=address['line2'],
                        grand_total=grand_total,
                    )
                sponsor_exists = True
                break
            except Sponsor.DoesNotExist:
                attempt += 1
                time.sleep(1)

        if sponsor_exists:
            self._subscription_confirmation_email(sponsor)

            return HttpResponse(
                content=f'Webhook received: {event["type"]} |\
                    SUCCESS: Verified order already in database',
                status=200)
        else:
            sponsor = None
            try:
                sponsor = Sponsor(
                    customer=customer,
                    subscription=subscription,
                    user_profile=username,
                    full_name=billing_details['name'],
                    email=billing_details['email'],
                    country=address['country'],
                    town_or_city=address['city'],
                    street_address1=address['line1'],
                    street_address2=address['line2'],
                    date=date,
                    grand_total=grand_total
                )

                sponsor.save()

            except Exception as e:
                if sponsor:
                    sponsor.delete()
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} | ERROR: {e}',
                    status=500)

        self._subscription_confirmation_email(sponsor)

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_succeeded(self, event):
        """
        Handle the payment_intent.succeeded webhook from Stripe
        """
        intent = event.data.object
        if 'cart' in intent.metadata:
            pid = intent.id
            cart = intent.metadata.cart
            save_info = intent.metadata.save_info

            billing_details = intent.charges.data[0].billing_details
            grand_total = round(intent.charges.data[0].amount / 100, 2)

            # Update profile information if save_info was checked
            profile = None
            username = intent.metadata.username
            if username != 'AnonymousUser':
                profile = UserProfile.objects.get(user__username=username)
                if save_info:
                    profile.default_country = billing_details.address.country
                    profile.default_town_or_city = billing_details.address.city
                    profile.default_street_address1 = billing_details.address.line1
                    profile.default_street_address2 = billing_details.address.line2
                    profile.save()

            order_exists = False
            attempt = 1
            while attempt <= 5:
                try:
                    order = Order.objects.get(
                        full_name__iexact=billing_details.name,
                        email__iexact=billing_details.email,
                        country__iexact=billing_details.address.country,
                        town_or_city__iexact=billing_details.address.city,
                        street_address1__iexact=billing_details.address.line1,
                        street_address2__iexact=billing_details.address.line2,
                        grand_total=grand_total,
                        original_cart=cart,
                        stripe_pid=pid,
                    )
                    order_exists = True
                    break
                except Order.DoesNotExist:
                    attempt += 1
                    time.sleep(1)

            if order_exists:
                self._send_confirmation_email(order)
                return HttpResponse(
                    content=f'Webhook received: {event["type"]} |\
                        SUCCESS: Verified order already in database',
                    status=200)
            else:
                order = None
                try:
                    order = Order.objects.get(
                        full_name=billing_details.name,
                        user_profile=profile,
                        email=billing_details.email,
                        country=billing_details.address.country,
                        town_or_city=billing_details.address.city,
                        street_address1=billing_details.address.line1,
                        street_address2=billing_details.address.line2,
                        grand_total=grand_total,
                        original_cart=cart,
                        stripe_pid=pid,
                    )
                    for item_id, item_data in json.loads(cart).items():
                        product = Product.objects.get(id=item_id)
                        if isinstance(item_data, int):
                            order_line_item = OrderLineItem(
                                order=order,
                                product=product,
                                quantity=item_data,
                            )
                            order_line_item.save()

                except Exception as e:
                    if order:
                        order.delete()
                    return HttpResponse(
                        content=f'Webhook received: {event["type"]} | ERROR: {e}',
                        status=500)
            self._send_confirmation_email(order)
        else:
            pid = intent.id

        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_intent_payment_failed(self, event):
        """
        Handle the payment_intent.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_invoice_paid(self, event):
        """
        Handle the invoice.paid webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_payment_failed(self, event):
        """
        Handle the invoice.payment_failed webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)

    def handle_subscription_deleted(self, event):
        """
        Handle the customer.subscription.deleted webhook from Stripe
        """
        return HttpResponse(
            content=f'Webhook received: {event["type"]}',
            status=200)
