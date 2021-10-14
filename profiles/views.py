from django.shortcuts import render


def profile(request):
    template = 'profiles/profile.html'
    return render(request, template)
