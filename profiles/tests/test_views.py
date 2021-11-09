from django.shortcuts import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.client import Client


class testViews(TestCase):
    """
    Test profile app views

    Methods:
        *test_get_profile_logged_out: Test profile view get response
                                      when user is logged ou;
        *test_get_profile_logged_in: Test profile view get response
                                     when user is logged in;
        *test_post_profile: Test profile view post response;
        *test_post_redeem_subscription: Test redeem_subscription
                                        view post response;
    """

    def test_get_profile_logged_out(self):
        """
        Test profile view get response when user is logged out
        """
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, '/accounts/login/?next=/profile/',
                             status_code=302,
                             target_status_code=200)

    def test_get_profile_logged_in(self):
        """
        Test profile view get response when user is logged in
        """
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile.html')
        self.assertContains(response,
                            '<h1 class="font-weight-bold">My Profile</h1>')

        url_name = self.client.get(reverse('profile'))
        self.assertEquals(url_name.status_code, 200)

    def test_post_profile(self):
        """
        Test profile view post response
        """
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

        form_data = {
            'default_full_name': 'John Lennon',
            'default_street_address1': 'Anywhere 1',
            'default_street_address2': 'Anywhere 2',
            'default_town_or_city': 'Anywhere city',
            'default_country': 'Anywhere country'
        }
        response = self.client.post('/profile/', data=form_data)
        self.assertEqual(response.status_code, 200)

    def test_post_redeem_subscription(self):
        """
        Test redeem_subscription view post response
        """
        self.client = Client()
        self.user = User.objects.create_user('john', 'lennon@thebeatles.com',
                                             'johnpassword')
        self.client.login(username='john', password='johnpassword')

        form_data = {
            'redeem_subs': 'sub_42462632527327',
            'last_digits': '4242'
        }
        response = self.client.post('/profile/redeem_subscription/',
                                    data=form_data)
        self.assertEqual(response.status_code, 302)
