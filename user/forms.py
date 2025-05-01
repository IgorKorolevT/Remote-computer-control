from .models import User
# from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
