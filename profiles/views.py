from django.shortcuts import render, get_object_or_404
from .models import UserProfile
from .forms import UserProfileForm
from django.contrib import messages


def profile(request):
    """ Display the user's profile. """
    profile_user = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        profileForm = UserProfileForm(request.POST, instance=profile_user)
        if profileForm.is_valid():
            profileForm.save()
            messages.success(request, 'Profile updated successfully')

    profileForm = UserProfileForm(instance=profile_user)
    orders = profile_user.orders.all()

    template = 'profiles/profile.html'
    context = {
        'profile': profile_user,
        'profileForm': profileForm,
        'orders': orders,
        'on_profile_page': True,
    }

    return render(request, template, context)
