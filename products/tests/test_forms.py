from django.test import TestCase
from products.forms import ProductForm, ParcelForm


class testProductForm(TestCase):
    """
    Test ProductForm

    Methods:
        *test_category_is_required: Test if category field is required;
        *test_sku_is_required: Test if sku field is required;
        *test_name_is_required: Test if name field is required;
        *test_description_is_required: Test if description field is required;
        *test_price_is_required: Test if price field is required;
    """
    def test_category_is_required(self):
        """
        Test if category field is required
        """

        form = ProductForm({'category': ""})
        self.assertFalse(form.is_valid())

    def test_sku_is_required(self):
        """
        Test if sku field is required
        """

        form = ProductForm({'sku': ""})
        self.assertFalse(form.is_valid())

    def test_name_is_required(self):
        """
        Test if name field is required
        """

        form = ProductForm({'name': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertEqual(form.errors['name'][0],
                         'This field is required.')

    def test_description_is_required(self):
        """
        Test if description field is required
        """

        form = ProductForm({'description': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors.keys())
        self.assertEqual(form.errors['description'][0],
                         'This field is required.')

    def test_price_is_required(self):
        """
        Test if price field is required
        """

        form = ProductForm({'price': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors.keys())
        self.assertEqual(form.errors['price'][0],
                         'This field is required.')


class testParcelForm(TestCase):
    """
    Test ParcelForm

    Methods:
        *test_sku_is_required: Test if sku field is required;
        *test_name_is_required: Test if name field is required;
        *test_description_is_required: Test if description field is required;
        *test_price_is_required: Test if price field is required;
    """

    def test_sku_is_required(self):
        """
        Test if sku field is required
        """

        form = ParcelForm({'sku': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('sku', form.errors.keys())
        self.assertEqual(form.errors['sku'][0],
                         'This field is required.')

    def test_name_is_required(self):
        """
        Test if name field is required
        """

        form = ParcelForm({'name': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors.keys())
        self.assertEqual(form.errors['name'][0],
                         'This field is required.')

    def test_description_is_required(self):
        """
        Test if description field is required
        """

        form = ParcelForm({'description': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('description', form.errors.keys())
        self.assertEqual(form.errors['description'][0],
                         'This field is required.')

    def test_price_is_required(self):
        """
        Test if price field is required
        """

        form = ParcelForm({'price': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('price', form.errors.keys())
        self.assertEqual(form.errors['price'][0],
                         'This field is required.')
