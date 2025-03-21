from django import forms
from django.contrib.auth.hashers import make_password

from .models import faculty
from AeroMaster.models import User


class FacultyForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = faculty
        fields = ['first_name', 'last_name', 'emp_id', 'email', 'password']

    def save(self, commit=True):
        faculty_instance = super().save(commit=False)
        if self.cleaned_data['password']:
            faculty_instance.password = make_password(self.cleaned_data['password'])
        if commit:
            faculty_instance.save()
        return faculty_instance

class StudentForm(forms.ModelForm):
    password = forms.CharField(required=False, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id_number', 'email', 'password']

    def save(self, commit=True):
        faculty_instance = super().save(commit=False)
        if self.cleaned_data['password']:
            faculty_instance.password = make_password(self.cleaned_data['password'])
        if commit:
            faculty_instance.save()
        return faculty_instance


