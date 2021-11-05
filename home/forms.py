from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)
    email_address = forms.EmailField(max_length=150)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)

    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        super().__init__(*args, **kwargs)
        placeholders = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email_address': 'Email Address',
            'message': 'message'
        }

        self.fields['first_name'].widget.attrs['autofocus'] = True
        self.fields['message'].widget.attrs['style'] = 'resize:none'
        for field in self.fields:
            self.fields[field].required = True
            placeholder = f'{placeholders[field]} *'
            self.fields[field].widget.attrs['placeholder'] = placeholder
            self.fields[field].widget.attrs['class'] = 'w-100 rounded-0 mt-5'
            self.fields[field].label = False
