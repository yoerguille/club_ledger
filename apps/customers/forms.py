from django import forms

from .models import Customer
from apps.core.forms.styles import INPUT_CLASSES

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer

        fields = [
            'name',
            'cif',
            'email',
            'phone',
            'adress',
            'contact_person',
        ]
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASSES

            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows']= 2