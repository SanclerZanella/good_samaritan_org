from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import send_mail, BadHeaderError
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from .forms import ContactForm


def index(request):
    """
    A view to render the index page
    """
    template = 'home/index.html'

    return render(request, template)


def about(request):
    """
    A view to render the about page
    """
    template = 'home/about.html'

    return render(request, template)


def faq(request):
    """
    A view to render the FAQ page
    """
    template = 'home/faq.html'

    return render(request, template)


def contact(request):
    """
    A view to render the contact page
    """

    if request.method == 'POST':
        form = ContactForm(request.POST)

        if form.is_valid():

            # Customer email
            cust_email = form.cleaned_data['email_address']

            # Load the email subject text file template and turn on in string
            subject = render_to_string(
                'home/contact_email/contact_email_subject.txt')

            data_form = {
                    'first_name': form.cleaned_data['first_name'],
                    'last_name': form.cleaned_data['last_name'],
                    'email': form.cleaned_data['email_address'],
                    'message': form.cleaned_data['message'],
                    }

            # Load the email body text file template and turn on in string
            body = render_to_string(
                'home/contact_email/contact_email_body.txt',
                {'data': data_form})

            try:
                # Send contact email
                send_mail(subject, body, cust_email,
                          [settings.DEFAULT_FROM_EMAIL])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')

            messages.success(request, "Message successfully sent,\
                Thank you for contact us!")
            return redirect("home")

    form = ContactForm()
    context = {
        'form': form,
    }

    template = 'home/contact.html'

    return render(request, template, context)
