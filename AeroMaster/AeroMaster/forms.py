from django import forms
from django.contrib.auth.hashers import make_password
from .models import User


class SignUpForm(forms.ModelForm):
    confirm_password = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.PasswordInput(),
        label="Confirm Password"
    )

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id_number', 'email', 'password', 'last_login']

    def clean_id_number(self):
        id_number = self.cleaned_data.get('id_number')
        if User.objects.filter(id_number=id_number).exists():
            raise forms.ValidationError("This ID Number is already in use.")
        return id_number

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already registered.")
        return email

    def clean_confirm_password(self):
        """ Validate that c_password matches password """
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match!")  # Error assigned to c_password

        return confirm_password

    def save(self, commit=True):
        """ Hash the password before saving the user """
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])  # Hash password
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['id_number', 'password']

