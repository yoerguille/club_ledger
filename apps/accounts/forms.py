from django import forms

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

        self.customer = customer
