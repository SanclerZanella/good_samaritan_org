from django.test import TestCase
from checkout.forms import OrderForm, SponsorForm


class testOrderForm(TestCase):
    """
    Test OrderForm

    Methods:
        *test_full_name_is_required: Test if full_name field is required;
        *test_email_is_required: Test if email field is required;
        *test_email_is_valid: Test if email field is valid;
        *test_street_address1_is_required: Test if street_address1
                                           field is required;
        *test_town_or_city_is_required: Test if town_or_city field is required;
        *test_country_is_required: Test if country field is required;
    """
    def test_full_name_is_required(self):
        """
        Test if full_name field is required
        """

        form = OrderForm({'full_name': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors.keys())
        self.assertEqual(form.errors['full_name'][0],
                         'This field is required.')

    def test_email_is_required(self):
        """
        Test if email field is required
        """

        form = OrderForm({'email': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())
        self.assertEqual(form.errors['email'][0],
                         'This field is required.')

    def test_email_is_valid(self):
        """
        Test if email field is valid
        """

        form = OrderForm({'email': "test_test.com"})

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())
        self.assertEqual(form.errors['email'][0],
                         'Enter a valid email address.')

    def test_street_address1_is_required(self):
        """
        Test if street_address1 field is required
        """

        form = OrderForm({'street_address1': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('street_address1', form.errors.keys())
        self.assertEqual(form.errors['street_address1'][0],
                         'This field is required.')

    def test_town_or_city_is_required(self):
        """
        Test if town_or_city field is required
        """

        form = OrderForm({'town_or_city': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('town_or_city', form.errors.keys())
        self.assertEqual(form.errors['town_or_city'][0],
                         'This field is required.')

    def test_country_is_required(self):
        """
        Test if country field is required
        """

        form = OrderForm({'country': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors.keys())
        self.assertEqual(form.errors['country'][0],
                         'This field is required.')


class testSponsorForm(TestCase):
    """
    Test SponsorForm

    Methods:
        *test_full_name_is_required: Test if full_name field is required;
        *test_email_is_required: Test if email field is required;
        *test_email_is_valid: Test if email field is valid;
        *test_street_address1_is_required: Test if street_address1
                                           field is required;
        *test_town_or_city_is_required: Test if town_or_city field is required;
        *test_country_is_required: Test if country field is required;
    """
    def test_full_name_is_required(self):
        """
        Test if full_name field is required
        """

        form = SponsorForm({'full_name': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('full_name', form.errors.keys())
        self.assertEqual(form.errors['full_name'][0],
                         'This field is required.')

    def test_email_is_required(self):
        """
        Test if email field is required
        """

        form = SponsorForm({'email': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())
        self.assertEqual(form.errors['email'][0],
                         'This field is required.')

    def test_email_is_valid(self):
        """
        Test if email field is valid
        """

        form = SponsorForm({'email': "test_test.com"})

        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors.keys())
        self.assertEqual(form.errors['email'][0],
                         'Enter a valid email address.')

    def test_street_address1_is_required(self):
        """
        Test if street_address1 field is required
        """

        form = SponsorForm({'street_address1': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('street_address1', form.errors.keys())
        self.assertEqual(form.errors['street_address1'][0],
                         'This field is required.')

    def test_town_or_city_is_required(self):
        """
        Test if town_or_city field is required
        """

        form = SponsorForm({'town_or_city': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('town_or_city', form.errors.keys())
        self.assertEqual(form.errors['town_or_city'][0],
                         'This field is required.')

    def test_country_is_required(self):
        """
        Test if country field is required
        """

        form = SponsorForm({'country': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('country', form.errors.keys())
        self.assertEqual(form.errors['country'][0],
                         'This field is required.')
