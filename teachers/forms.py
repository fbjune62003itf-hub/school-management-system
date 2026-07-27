from django import forms
from .models import Teacher
from accounts.models import CustomUser


class TeacherForm(forms.ModelForm):

    user = forms.ModelChoiceField(
        queryset=CustomUser.objects.filter(user_type="teacher"),
        empty_label="Select Teacher Login Account"
    )

    class Meta:
        model = Teacher
        fields = "__all__"