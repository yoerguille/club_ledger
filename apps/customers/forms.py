from django import forms

from .models import Customer

INPUT_CLASSES = (
    "block w-full rounded-lg border border-gray-300 "
    "bg-gray-50 p-2.5 text-sm text-gray-900 "
    "focus:border-btn-primary focus:ring-btn-primary "
    "dark:border-white/10 dark:bg-dark-secondary "
    "dark:text-white dark:placeholder:text-secondary "
    "dark:scheme-dark"
)
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