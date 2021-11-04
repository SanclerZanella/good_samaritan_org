from django.shortcuts import render


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
