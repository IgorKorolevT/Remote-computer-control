from .models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class UserUpdateForm(UserChangeForm):
    # Hide password
    password = None

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")


class ComputerAddForm(forms.Form):
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
