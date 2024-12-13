from django import forms
from .models import Service
from django.contrib.auth.models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'confirm_password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

class OTPForm(forms.Form):
    otp = forms.CharField(max_length=6, required=True)

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['name', 'payment_terms', 'price', 'package', 'tax', 'image', 'active']