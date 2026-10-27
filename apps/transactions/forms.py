from django import forms
from apps.core.forms.styles import INPUT_CLASSES
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
    def __init__(self, *args, customer=None, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASSES

            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows']= 2

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
    def __init__(self, *args, customer=None, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASSES

            if isinstance(field.widget, forms.Textarea):
                field.widget.attrs['rows']= 2

    def clean_payment_method(self):

        payment_method = self.cleaned_data.get("payment_method")

        if not payment_method:
            raise forms.ValidationError(
                "Debes seleccionar un método de pago."
            )
            
        return payment_method
        


