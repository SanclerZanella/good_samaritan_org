from django.shortcuts import render, get_object_or_404
from .models import UserProfile


def profile(request):
    """ Display the user's profile. """
    profile_user = get_object_or_404(UserProfile, user=request.user)
    print(request.user)

    template = 'profiles/profile.html'
    context = {
        'profile': profile_user,
    }

    return render(request, template, context)
