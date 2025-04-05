from django import forms
from django.contrib.auth.hashers import make_password

from .models import faculty, AeroMaster_admin
from AeroMaster.models import User, Question


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


CORRECT_ANSWER_CHOICES = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D'),
]


class QuestionForm(forms.ModelForm):
    correct_answer = forms.ChoiceField(choices=CORRECT_ANSWER_CHOICES)

    class Meta:
        model = Question
        fields = ['text', 'option_a', 'option_b', 'option_c', 'option_d', 'correct_answer', 'subject']


class AeroMasterAdminForm(forms.Form):
    username = forms.CharField(max_length=50, required=True)
    password = forms.CharField(max_length=100, required=True, widget=forms.PasswordInput)
