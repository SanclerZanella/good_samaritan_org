from django.shortcuts import reverse
from django.test import TestCase
from products.models import Product, Category, Parcel
from djstripe.models import Product as Sponsorship
from django.contrib.auth.models import User
from django.test.client import Client
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template


class testViews(TestCase):
    """
    Test home app views

    Methods:
        *test_get_all_products: Test all_products view get response;
        *test_get_about: Test about view get response;
        *test_get_faq: Test faq view get response;
        *test_get_contact: Test contact view get response;
        *test_post_contact: Test contact view post response;
    """

    def test_get_all_products(self):
        """
        Test all_products view get response
        """
        category = Category.objects.create(name='mock',
                                           friendly_name='mock')
        Product.objects.create(category=category,
                               sku='mock_pp5001340155',
                               name='mock_product',
                               description='mock_product',
                               price=1.90)

        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/products.html')
        self.assertContains(response, '<h1>Products</h1>')

        url_name = self.client.get(reverse('products'))
        self.assertEquals(url_name.status_code, 200)

    def test_get_all_products_sort_param(self):
        """
        Test all_products view sort parameter in get response
        """
        category = Category.objects.create(name='mock',
                                           friendly_name='mock')
        Product.objects.create(category=category,
                               sku='mock_pp5001340155',
                               name='mock_product',
                               description='mock_product',
                               price=1.90)

        response = self.client.get('/products/?sort=price&direction=asc')
        self.assertEqual(response.status_code, 200)

    def test_get_all_products_category_param(self):
        """
        Test all_products view category parameter in get response
        """
        category = Category.objects.create(name='baby_child',
                                           friendly_name='baby & child')
        Product.objects.create(category=category,
                               sku='mock_pp5001340155',
                               name='mock_product',
                               description='mock_product',
                               price=1.90)

        response = self.client.get('/products/?category=baby_child')
        self.assertEqual(response.status_code, 200)

    def test_get_all_products_q_param(self):
        """
        Test all_products view q parameter in get response
        """
        category = Category.objects.create(name='mock',
                                           friendly_name='mock')
        Product.objects.create(category=category,
                               sku='mock_pp5001340155',
                               name='chicken',
                               description='mock_product',
                               price=1.90)

        response = self.client.get('/products/?q=chicken')
        self.assertEqual(response.status_code, 200)

    def test_get_all_products_urgent_param(self):
        """
        Test all_products view urgent parameter in get response
        """
        category = Category.objects.create(name='mock',
                                           friendly_name='mock')
        Product.objects.create(category=category,
                               sku='mock_pp5001340155',
                               name='chicken',
                               description='mock_product',
                               m_needed=True,
                               price=1.90)

        response = self.client.get('/products/?urgent=most_needed')
        self.assertEqual(response.status_code, 200)

    def test_get_parcels(self):
        """
        Test parcels view get response
        """
        category = Category.objects.create(name='mock',
                                           friendly_name='mock')
        Product.objects.create(category=category,
                               sku='mock_pp5001340155',
                               name='chicken',
                               description='mock_product',
                               m_needed=True,
                               price=1.90)
        Parcel.objects.create(sku='mock_pp5001340155_pc',
                              name='mock_parcel',
                              description='mock_parcel',
                              price=1.90,
                              items="1")

        response = self.client.get('/products/parcels/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'products/parcels.html')
        self.assertContains(response, '<h1>Family Parcels</h1>')

        url_name = self.client.get(reverse('parcels'))
        self.assertEquals(url_name.status_code, 200)

    def test_get_parcels_param(self):
        """
        Test parcels view parcel parameter in get response
        """
        category = Category.objects.create(name='mock',
                                           friendly_name='mock')
        Product.objects.create(category=category,
                               sku='mock_pp5001340155',
                               name='chicken',
                               description='mock_product',
                               m_needed=True,
                               price=1.90)
        Parcel.objects.create(sku='mock_pp5001340155_pc',
                              name='mock_parcel',
                              description='mock_parcel',
                              price=1.90,
                              items="1")

        response = self.client.get('/products/parcels/?parcel=parcel_1')
        self.assertEqual(response.status_code, 200)

    def test_get_product_details(self):
        """
        Test product_details view
        """
        category = Category.objects.create(name='mock',
                                           friendly_name='mock')
        product = Product.objects.create(category=category,
                                         sku='mock_pp5001340155',
                                         name='mock_product',
                                         description='mock_product',
                                         price=1.90)

        response = self.client.get(f'/products/{product.id}/')
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'products/product_details.html')
        el = f'<h1 class="text-center font-weight-bold">{ product.name }</h1>'
        self.assertContains(response, el)

        url_name = self.client.get(reverse('product_details',
                                   args=(str(product.id))))
        self.assertEquals(url_name.status_code, 200)

    def test_get_product_management(self):
        """
        Test product_mangement view
        """
        self.client = Client()
        self.user = User.objects.create_superuser('myuser',
                                                  'myemail@test.com',
                                                  'mypassword')
        self.client.login(username='myuser', password='mypassword')

        response = self.client.get('/products/product_management/')
        self.assertEqual(response.status_code, 200)

        self.assertTemplateUsed(response, 'products/product_management.html')
        el = '<h2 id="mg-title" class="font-weight-bold">Product Management</h2>'
        self.assertContains(response, el)

        url_name = self.client.get(reverse('product_management'))
        self.assertEquals(url_name.status_code, 200)

    def test_get_product_management_sort_param(self):
        """
        Test product_management view sort parameter in get response
        """
        response = self.client.get(
            '/products/product_management/?sort=price&direction=asc')
        self.assertEqual(response.status_code, 302)

    def test_get_product_management_category_param(self):
        """
        Test product_management view category parameter in get response
        """
        response = self.client.get(
            '/products/product_management/?category=baby_child')
        self.assertEqual(response.status_code, 302)

    def test_get_product_management_q_param(self):
        """
        Test product_management view q parameter in get response
        """
        response = self.client.get('/products/product_management/?q-mg=Baby')
        self.assertEqual(response.status_code, 302)

    def test_get_product_management_urgent_param(self):
        """
        Test product_management view urgent parameter in get response
        """
        response = self.client.get(
            '/products/product_management/?urgent=most_needed')
        self.assertEqual(response.status_code, 302)

    def test_get_add_product(self):
        """
        Test add_product view
        """
        self.client = Client()
        self.user = User.objects.create_superuser('myuser',
                                                  'myemail@test.com',
                                                  'mypassword')
        self.client.login(username='myuser', password='mypassword')

        response = self.client.post('/products/add_product/')
        self.assertEqual(response.status_code, 302)

        url_name = self.client.get(reverse('product_management'))
        self.assertEquals(url_name.status_code, 200)
