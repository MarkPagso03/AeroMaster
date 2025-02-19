from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    id_number = forms.CharField(max_length=20, required=True, label="ID Number")
    email = forms.EmailField(max_length=254, required=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'id_number', 'email', 'password']

    def clean_idnumber(self):
        id_number = self.cleaned_data.get('id_number')
        if CustomUser.objects.filter(idnumber=id_number).exists():
            raise forms.ValidationError("This ID Number is already in use.")
        return id_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email
