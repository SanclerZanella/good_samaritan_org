from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_countries.fields import CountryField


class UserProfile(models.Model):
    """
    Order Line Item Model

    Attributes:
        *user: A foreign key representing the related user field;
        *default_street_address1: A string representing
                                  the first street address;
        *default_street_address2: A string representing
                                  the second street address;
        *default_town_or_city: A string representing the town or city;
        *default_country: A string representing the country;

    Methods:
        *_generate_order_number: Generate a random, unique order number
                                 using UUID;
        *save: Override the original save method to set the lineitem total
               and update the order total;
        *__str__: Display the object's headline in the admin interface,
                  it returns a nice, human-readable representation of
                  the model.
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    default_street_address1 = models.CharField(max_length=80, null=True,
                                               blank=True)
    default_street_address2 = models.CharField(max_length=80, null=True,
                                               blank=True)
    default_town_or_city = models.CharField(max_length=40, null=True,
                                            blank=True)
    default_country = CountryField(blank_label='Country *', null=True,
                                   blank=True)

    def __str__(self):
        """
        Display the object's headline in the admin interface,
        it returns a nice, human-readable representation of
        the model.
        """
        return self.user.username


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal to create or update the user profile
    """
    if created:
        UserProfile.objects.create(user=instance)
    # Existing users: just save the profile
    instance.userprofile.save()
