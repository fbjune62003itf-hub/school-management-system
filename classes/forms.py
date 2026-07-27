from django import forms
from .models import SchoolClass


class SchoolClassForm(forms.ModelForm):
    class Meta:
        model = SchoolClass
        fields = "__all__"