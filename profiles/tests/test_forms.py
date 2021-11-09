from django.test import TestCase
from profiles.forms import RedeemForm


class testRedeemForm(TestCase):
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
