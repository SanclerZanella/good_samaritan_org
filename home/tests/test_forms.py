from django.test import TestCase
from home.forms import ContactForm


class testContactForm(TestCase):
    """
    Test contact form

    Methods:
        *test_first_name_is_required: Test if first name field is required;
        *test_last_name_is_required: Test if last name field is required;
        *test_email_address_is_required: Test if email field is required;
        *test_email_address_is_valid: Test if email field is valid;
        *test_message_is_required: Test if message field is required;
    """
    def test_first_name_is_required(self):
        """
        Test if first name field is required
        """

        form = ContactForm({'first_name': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('first_name', form.errors.keys())
        self.assertEqual(form.errors['first_name'][0],
                         'This field is required.')

    def test_last_name_is_required(self):
        """
        Test if last name field is required
        """

        form = ContactForm({'last_name': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('last_name', form.errors.keys())
        self.assertEqual(form.errors['last_name'][0],
                         'This field is required.')

    def test_email_address_is_required(self):
        """
        Test if email field is required
        """

        form = ContactForm({'email_address': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('email_address', form.errors.keys())
        self.assertEqual(form.errors['email_address'][0],
                         'This field is required.')

    def test_email_address_is_valid(self):
        """
        Test if email field is valid
        """

        form = ContactForm({'email_address': "test_test.com"})

        self.assertFalse(form.is_valid())
        self.assertIn('email_address', form.errors.keys())
        self.assertEqual(form.errors['email_address'][0],
                         'Enter a valid email address.')

    def test_message_is_required(self):
        """
        Test if message field is required
        """

        form = ContactForm({'message': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors.keys())
        self.assertEqual(form.errors['message'][0], 'This field is required.')
