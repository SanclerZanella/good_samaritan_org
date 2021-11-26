from django.test import TestCase
from profiles.forms import RedeemForm, UserProfileForm


class TestRedeemForm(TestCase):
    """
    Test RedeemForm

    Methods:
        *test_redeem_subs_is_required: Test if redeem_subs field is required;
        *test_last_digits_is_required: Test if last_digits field is required;
        *test_last_digits_max_length: Test last_digits field max length;
        *test_last_digits_min_length: Test last_digits field min length;
    """
    def test_redeem_subs_is_required(self):
        """
        Test if redeem_subs field is required
        """

        form = RedeemForm({'redeem_subs': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('redeem_subs', form.errors.keys())
        self.assertEqual(form.errors['redeem_subs'][0],
                         'This field is required.')

    def test_last_digits_is_required(self):
        """
        Test if last_digits field is required
        """

        form = RedeemForm({'last_digits': ""})

        self.assertFalse(form.is_valid())
        self.assertIn('last_digits', form.errors.keys())
        self.assertEqual(form.errors['last_digits'][0],
                         'This field is required.')

    def test_last_digits_max_length(self):
        """
        Test last_digits field max length
        """

        form = RedeemForm({'redeem_subs': "sub_312123133124",
                           'last_digits': "12345"})

        self.assertFalse(form.is_valid())
        self.assertIn('last_digits', form.errors.keys())
        self.assertEqual(form.errors['last_digits'][0],
                         'Ensure this value is less than or equal to 4.')

    def test_last_digits_min_length(self):
        """
        Test last_digits field min length
        """

        form = RedeemForm({'redeem_subs': "sub_312123133124",
                           'last_digits': "123"})

        self.assertFalse(form.is_valid())
        self.assertIn('last_digits', form.errors.keys())
        self.assertEqual(form.errors['last_digits'][0],
                         'Ensure this value is less than or equal to 4.')


class TestUserProfileForm(TestCase):
    """
    Test UserProfileForm

    Methods:
        *test_country_is_not_valid: Test if country field is not valid;
        *test_country_is_valid: Test if country field is valid;
    """
    def test_country_is_not_valid(self):
        """
        Test if country field is not valid
        """

        form = UserProfileForm({
            'default_full_name': 'John Lennon',
            'default_street_address1': 'Anywhere 1',
            'default_street_address2': 'Anywhere 2',
            'default_town_or_city': 'Anywhere city',
            'default_country': 'Anywhere country'
        })

        self.assertFalse(form.is_valid())
        self.assertIn('default_country', form.errors.keys())
        msg1 = 'Select a valid choice. Anywhere country '
        msg2 = 'is not one of the available choices.'
        msg = f'{msg1}{msg2}'
        self.assertEqual(form.errors['default_country'][0], msg)

    def test_country_is_valid(self):
        """
        Test if country field is valid
        """

        form = UserProfileForm({
            'default_full_name': 'John Lennon',
            'default_street_address1': 'Anywhere 1',
            'default_street_address2': 'Anywhere 2',
            'default_town_or_city': 'Anywhere city',
            'default_country': 'BR'
        })

        self.assertTrue(form.is_valid())
