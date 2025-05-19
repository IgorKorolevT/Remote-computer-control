from .models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]


class ContactForm(forms.Form):
    name = forms.CharField(required=True,
                           label="Computer Name",
                           help_text="Enter the name of the computer.",
                           )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Password",
        help_text="Enter the password for this computer.",
    )