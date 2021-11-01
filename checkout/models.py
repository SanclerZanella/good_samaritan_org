from django.db import models
from django.db.models import Sum
from products.models import Product, Parcel
from profiles.models import UserProfile
from django_countries.fields import CountryField
from djstripe.models import Customer, Subscription
import uuid


class Order(models.Model):
    """
    Order Model

    Attributes:
        *order_number: Random, unique, auto-generated id to an Order;
        *user_profile: Database field representing the profile of the
                       user who made the order, if the user is logged;
        *full_name: A string representing the user full name;
        *email: A string representing the user email;
        *country: A string representing the user country;
        *town_or_city: A string representing the user town or city;
        *street_address1: A string representing the user first part of
                          street address;
        *street_address2: A string representing the user second part of
                          street address;
        *date: A date representing when the order was created;
        *grand_total: A decimal number representing the order grand total;
        *original_cart: A text-field representing the list of products
                        in the order;
        *stripe_pid: A string representing the payment id from stripe.

    Methods:
        *_generate_order_number: Generate a random, unique order number
                                 using UUID;
        *update_total: Update grand total each time a line item is added;
        *save: Override the original save method to set the order number
               if it hasn't been set already.
        *__str__: Display the object's headline in the admin interface,
                  it returns a nice, human-readable representation of
                  the model;
    """

    order_number = models.CharField(max_length=32, null=False, editable=False)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='orders')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
    original_cart = models.TextField(null=False, blank=False, default='')
    stripe_pid = models.CharField(max_length=254, null=False, blank=False,
                                  default='')

    def _generate_order_number(self):
        """
        Generate a random, unique order number using UUID
        """
        return uuid.uuid4().hex.upper()

    def update_total(self):
        """
        Update grand total each time a line item is added.
        """

        self.grand_total = self.lineitems.aggregate(
            Sum('lineitem_total'))['lineitem_total__sum'] or 0
        self.save()

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the order number
        if it hasn't been set already.
        """
        if not self.order_number:
            self.order_number = self._generate_order_number()
        super().save(*args, **kwargs)

    def __str__(self):
        """
        Display the object's headline in the admin interface,
        it returns a nice, human-readable representation of
        the model;
        """
        return self.order_number


class OrderLineItem(models.Model):
    """
    Order Line Item Model

    Attributes:
        *order: A foreign key representing the related order field;
        *product: A foreign key representing the related product field;
        *parcel: A foreign key representing the related parcel field;
        *quantity: An integer representing the product or parcel quantity;
        *lineitem_total: An decimal representing the product total price;

    Methods:
        *_generate_order_number: Generate a random, unique order number
                                 using UUID;
        *save: Override the original save method to set the lineitem total
               and update the order total;
        *__str__: Display the object's headline in the admin interface,
                  it returns a nice, human-readable representation of
                  the model.
    """

    order = models.ForeignKey(Order, null=False, blank=False,
                              on_delete=models.CASCADE,
                              related_name='lineitems')
    product = models.ForeignKey(Product, null=True, blank=True,
                                on_delete=models.CASCADE)
    parcel = models.ForeignKey(Parcel, null=True, blank=True,
                               on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=False, default=0)
    lineitem_total = models.DecimalField(max_digits=6, decimal_places=2,
                                         null=False, blank=False,
                                         editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the lineitem total
        and update the order total.
        """

        if self.product is not None:
            self.lineitem_total = self.product.price * self.quantity
        else:
            self.lineitem_total = self.parcel.price * self.quantity

        super().save(*args, **kwargs)

    def __str__(self):
        """
        Display the object's headline in the admin interface,
        it returns a nice, human-readable representation of
        the model.
        """
        if self.product is not None:
            return f'SKU {self.product.sku} on order {self.order.order_number}'
        else:
            return f'SKU {self.parcel.sku} on order {self.order.order_number}'


class Sponsor(models.Model):
    """
    Sponsor Model

    Attributes:
        *customer: A foreign key representing the related customer field;
        *subscription: A foreign key representing the related
                       subscription field;
        *user_profile: Database field representing the profile of the
                       user who made the subscrtiption,
                       if the user is logged;
        *full_name: A string representing the user full name;
        *email: A string representing the user email;
        *country: A string representing the user country;
        *town_or_city: A string representing the user town or city;
        *street_address1: A string representing the user first part of
                          street address;
        *street_address2: A string representing the user second part of
                          street address;
        *date: A date representing when the subscription was created;
        *grand_total: A decimal number representing the subscription
                      grand total;
    """

    customer = models.ForeignKey(Customer, null=True, blank=True,
                                 on_delete=models.SET_NULL)
    subscription = models.ForeignKey(Subscription, null=True, blank=True,
                                     on_delete=models.SET_NULL)
    user_profile = models.ForeignKey(UserProfile, on_delete=models.SET_NULL,
                                     null=True, blank=True,
                                     related_name='sponsorship')
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(max_length=254, null=False, blank=False)
    country = CountryField(blank_label='Country *', null=False, blank=False)
    town_or_city = models.CharField(max_length=40, null=False, blank=False)
    street_address1 = models.CharField(max_length=80, null=False, blank=False)
    street_address2 = models.CharField(max_length=80, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    grand_total = models.DecimalField(max_digits=10, decimal_places=2,
                                      null=False, default=0)
