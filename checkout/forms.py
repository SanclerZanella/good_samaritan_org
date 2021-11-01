from django import forms
from .models import Order, Sponsor


class OrderForm(forms.ModelForm):
    """
    Order form

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

        model = Order
        fields = ('full_name', 'email', 'street_address1',
                  'street_address2', 'town_or_city',
                  'country',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False


class SponsorForm(forms.ModelForm):
    """
    Sponsor form

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

        model = Sponsor
        fields = ('full_name', 'email', 'street_address1',
                  'street_address2', 'town_or_city',
                  'country',)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
        }

        self.fields['full_name'].widget.attrs['autofocus'] = True
        for field in self.fields:
            if field != 'country':
                if self.fields[field].required:
                    placeholder = f'{placeholders[field]} *'
                else:
                    placeholder = placeholders[field]
                self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'
            self.fields[field].label = False
