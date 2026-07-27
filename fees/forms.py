from django import forms
from .models import Fee


class FeeForm(forms.ModelForm):
    class Meta:
        model = Fee
        fields = "__all__"

        widgets = {
            "payment_date": forms.DateInput(attrs={"type": "date"}),
        }