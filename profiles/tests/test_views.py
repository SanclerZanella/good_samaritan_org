from django.shortcuts import reverse
from django.test import TestCase


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
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)
