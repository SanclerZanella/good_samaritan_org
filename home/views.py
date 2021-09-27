from django.shortcuts import render
from django.conf import settings


def index(request):
    """
    A view to return the index page
    """
    template = 'home/index.html'
    context = {
        'MEDIA_URL': settings.MEDIA_URL,
    }

    return render(request, template, context)
