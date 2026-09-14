from django import forms

from .models import Customer

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
        base_classes = (
            "w-full rounded-lg border border-gray-300 bg-white/5 "
            "px-3 py-2.5 text-sm text-gray-100 placeholder-gray-500 "
            "focus:border-blue-500 focus:outline-none focus:ring-2 "
            "focus:ring-blue-500/20"
        )
        for field in self.fields.values():
            field.widget.attrs.update({"class": base_classes})