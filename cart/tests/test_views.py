from django.shortcuts import reverse
from django.test import TestCase
from products.models import Product, Category


class testViews(TestCase):
    """
    Test home app views

    Methods:
        *test_get_cart: Test cart view;
        *test_post_add_to_cart: Test add to cart view;
        *test_post_add_all_to_cart: Test add all view;
        *test_post_update_cart: Test update view;
    """

    def test_get_cart(self):
        """
        Test cart view
        """
        response = self.client.get('/cart/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart.html')
        self.assertContains(response, '<h1>Shopping Cart</h1>')

        url_name = self.client.get(reverse('view_cart'))
        self.assertEquals(url_name.status_code, 200)

    def test_post_add_to_cart(self):
        """
        Test add to cart view
        """
        category = Category.objects.create(name='mock',
                                           friendly_name='mock')
        product = Product.objects.create(category=category,
                                         sku='mock_pp5001340155',
                                         name='mock_product',
                                         description='mock_product',
                                         price=1.90)

        form_data = {
            'quantity': '1',
            'redirect_url': f'/products/{product.id}'
        }
        response = self.client.post(f'/cart/add/{product.id}/{product.sku}/',
                                    data=form_data)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/products/{product.id}',
                             status_code=302,
                             target_status_code=301)

        session = self.client.session
        self.assertIn('cart', session)

        self.assertIsInstance(session['cart'], dict)

        self.assertIn('products', session['cart'])
        self.assertIn('parcels', session['cart'])

    def test_post_add_all_to_cart(self):
        """
        Test add all to cart view
        """
        form_data = {
            'redirect_url': '/products/',
            'items_list': '[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]'
        }
        response = self.client.post('/cart/add_all/', data=form_data)
        self.assertEqual(response.status_code, 302)

        session = self.client.session
        self.assertIn('cart', session)

        self.assertIsInstance(session['cart'], dict)

        self.assertIn('products', session['cart'])
        self.assertIn('parcels', session['cart'])

    def test_post_update_cart(self):
        """
        Test update cart view
        """
        category = Category.objects.create(name='mock',
                                           friendly_name='mock')
        product = Product.objects.create(category=category,
                                         sku='mock_pp5001340155',
                                         name='mock_product',
                                         description='mock_product',
                                         price=1.90)

        form_data = {
            'redirect_url': '/cart/',
            'quantity': '1'
        }
        url = f'/cart/update_cart/{product.id}/{product.sku}'
        response = self.client.post(url, data=form_data)
        self.assertEqual(response.status_code, 302)

        session = self.client.session
        self.assertIn('cart', session)

        self.assertIsInstance(session['cart'], dict)

        self.assertIn('products', session['cart'])
        self.assertIn('parcels', session['cart'])
