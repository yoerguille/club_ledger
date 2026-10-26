from django import forms

from .models import Season

from django import forms
from apps.core.forms.styles import INPUT_CLASSES
from apps.seasons.models import Season


class SeasonForm(forms.ModelForm):
    class Meta:
        model = Season

        fields = [
            "name",
            "start_date",
            "end_date",
        ]

        widgets = {
            "start_date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
            "end_date": forms.DateInput(
                attrs={"type": "date"},
                format="%Y-%m-%d",
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = INPUT_CLASSES

    def clean(self):
        cleaned_data = super().clean()

        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date <= start_date:
            self.add_error(
                "end_date",
                "La fecha de finalización debe ser posterior a la fecha de inicio.",
            )

        return cleaned_data