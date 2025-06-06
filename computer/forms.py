from django import forms

from computer.models import Computer


class ComputerAddForm(forms.Form):
    name = forms.CharField(
        required=True,
        label="Computer Name",
        help_text="Enter the name of the computer.",
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        required=True,
        label="Password",
        help_text="Enter the password for this computer.",
    )


class ComputerUpdateForm(forms.ModelForm):
    class Meta:
        model = Computer
        exclude = ("channel_name", "users", "password")
