from django import forms
from apps.core.forms.styles import INPUT_CLASSES
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account

        fields = [
            'season',
            'name',
            'notes',
        ]

    def __init__(self, *args, customer=None, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASSES

            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows']= 2