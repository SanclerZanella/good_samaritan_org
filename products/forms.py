from django import forms
from .models import (Product, Category, Parcel)


class ProductForm(forms.ModelForm):
    """
    ProductForm

    Attributes:
        *image: Represents an add image input

    Sub-classes:
        *Meta: Represent related model and form fields
               caught from related model.

    Methods:
        *__init__: Add categories friendly name to categories list.
    """

    class Meta:
        """
        Meta

        Attributes:
            *Model: Model related to the form ;
            *fields: Representation of the fields in the form
                     caught from related model.
        """
        model = Product
        fields = '__all__'

    image = forms.ImageField(label='Image', required=False)

    def __init__(self, *args, **kwargs):
        """
        Add categories friendly name to categories list
        """

        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        self.fields['category'].choices = friendly_names
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'


class ParcelForm(forms.ModelForm):
    """
    ParcelForm

    Sub-classes:
        *Meta: Represent related model and form fields
               caught from related model.

    Methods:
        *__init__: Add a class to the fields.
    """

    class Meta:
        """
        Meta

        Attributes:
            *Model: Model related to the form ;
            *fields: Representation of the fields in the form
                     caught from related model.
        """
        model = Parcel
        fields = ('sku', 'name', 'description',
                  'price')

    def __init__(self, *args, **kwargs):
        """
        Add a class to the fields
        """
        super().__init__(*args, **kwargs)

        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
