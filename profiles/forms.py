from django import forms
from .models import UserProfile
from django.core.validators import (MaxValueValidator,
                                    MinValueValidator)


class UserProfileForm(forms.ModelForm):
    """
    UserProfileForm

    Sub-classes:
        *Meta: Represent related model and form fields
               caught from related model.

    Methods:
        *__init__: Add placeholders and classes, remove auto-generated
                   labels and set autofocus on first field;
    """

    class Meta:
        """
        Meta

        Attributes:
            *Model: Model related to the form ;
            *fields: Representation of the fields in the form
                    caught from related model.
        """
        model = UserProfile
        exclude = ('user',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'default_full_name': 'Full Name',
            'default_street_address1': 'Street Address 1',
            'default_street_address2': 'Street Address 2',
            'default_town_or_city': 'Town or City',
            'default_country': 'country',
        }

        self.fields['default_full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'default_country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'w-100 rounded-0 mt-5'
            self.fields[field].label = False


class RedeemForm(forms.Form):
    """
    Contact form

    Attributes:
        *redeem_subs: A string indicating the subscription id;
        *last_digits: An integer indicating the last 4 digits of the card.

    Methods:
        *__init__: Add placeholders and classes, remove auto-generated
                labels and set autofocus on first field;
    """

    redeem_subs = forms.CharField(max_length=100,
                                  label='Sponsorship Id:')
    last_digits = forms.IntegerField(validators=[MaxValueValidator(4),
                                                 MinValueValidator(4)],
                                     label='Last 4 digits of the card\
                                        used to pay the sponsorship:')

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        ph = 'Last 4 digits of the card used to pay the sponsorship'
        placeholders = {
            'redeem_subs': 'Sponsorship Id',
            'last_digits': ph
        }

        for field in self.fields:
            self.fields[field].required = True
            placeholder = f'{placeholders[field]} *'
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'w-100 rounded-0'
