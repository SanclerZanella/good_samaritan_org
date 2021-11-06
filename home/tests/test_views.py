from django.shortcuts import reverse
from django.test import TestCase
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import get_template


class testViews(TestCase):
    """
    Test home app views

    Methods:
        *test_get_index: Test index view get response;
        *test_get_about: Test about view get response;
        *test_get_faq: Test faq view get response;
        *test_get_contact: Test contact view get response;
        *test_post_contact: Test contact view post response;
    """

    def test_get_index(self):
        """
        Test index view get response
        """
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/index.html')
        self.assertContains(response, '<h2>Ways You Can Support</h2>')

        url_name = self.client.get(reverse('home'))
        self.assertEquals(url_name.status_code, 200)

    def test_get_about(self):
        """
        Test about view get response
        """
        response = self.client.get('/about/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/about.html')
        self.assertContains(response, '<h1>Who We Are</h1>')

        url_name = self.client.get(reverse('about'))
        self.assertEquals(url_name.status_code, 200)

    def test_get_faq(self):
        """
        Test faq view get response
        """
        response = self.client.get('/faq/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/faq.html')
        self.assertContains(response,
        '<h1 class="font-weight-bold">Frequently Asked Questions</h1>')

        url_name = self.client.get(reverse('faq'))
        self.assertEquals(url_name.status_code, 200)

    def test_get_contact(self):
        """
        Test contact view get response
        """
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home/contact.html')
        self.assertContains(response,
        '<h2 class="font-weight-bold contact-title">Contact Us</h2>')

        url_name = self.client.get(reverse('contact'))
        self.assertEquals(url_name.status_code, 200)

    def test_post_contact(self):
        """
        Test contact view post response
        """
        data_form = {
                    'first_name': 'Test User',
                    'last_name': 'User Test',
                    'email': 'test@test.com',
                    'message': 'Mock message for test',
                    }

        response = self.client.post('/contact/', data_form)

        cust_email = 'test@test.com'

        email_subject = get_template(
            'home/contact_email/contact_email_subject.txt')
        self.assertTrue(email_subject)

        email_body = get_template('home/contact_email/contact_email_body.txt')
        self.assertTrue(email_body)

        subject = render_to_string(
                'home/contact_email/contact_email_subject.txt')
        self.assertTrue(subject)

        body = render_to_string(
                'home/contact_email/contact_email_body.txt',
                {'data': data_form})
        self.assertTrue(body)

        default_email = settings.DEFAULT_FROM_EMAIL
        self.assertTrue(default_email)

        email_sent = send_mail(subject, body, cust_email,
                               [settings.DEFAULT_FROM_EMAIL])
        self.assertTrue(email_sent)

        self.assertEqual(response.status_code, 200)
