from django import forms
from .models import Examination


class ExaminationForm(forms.ModelForm):

    student_name = forms.CharField(
        label="Student Name",
        max_length=100,
        help_text="Enter student's first name or surname"
    )

    class Meta:

        model = Examination

        fields = [
            "school_class",
            "student_name",
            "subject",
            "term",
            "academic_year",
            "score",
        ]

        widgets = {

            "academic_year": forms.TextInput(
                attrs={
                    "placeholder": "Example: 2026/2027"
                }
            ),

            "score": forms.NumberInput(
                attrs={
                    "min": 0,
                    "max": 100
                }
            ),
        }