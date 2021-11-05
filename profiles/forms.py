from django import forms
from .models import UserProfile


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
