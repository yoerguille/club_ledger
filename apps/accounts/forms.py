from django import forms

from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account

        fields = [
            'season',
            'notes',
        ]

    def __init__(self, *args, customer=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.customer = customer

    def clean(self):
        cleaned_data = super().clean()

        season = cleaned_data.get("season")

        if (
            self.customer
            and season
            and Account.objects.filter(
                customer = self.customer,
                season = season,
            ).exists()
        ):
            self.add_error(
                "season",
                "Este cliente ya tiene una cuenta en esa temporada."
            )
        
        return cleaned_data