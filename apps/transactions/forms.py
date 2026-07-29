from django import forms

from .models import Transaction


class ChargeForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "date",
            "description",
            "amount",
            "notes",
        ]

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "date",
            "description",
            "amount",
            "payment_method",
            "notes",
        ]

        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_payment_method(self):

        payment_method = self.cleaned_data.get("payment_method")

        if not payment_method:
            raise forms.ValidationError(
                "Debes seleccionar un método de pago."
            )
            
        return payment_method
        


