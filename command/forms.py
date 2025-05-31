from django import forms

from command.models import Command


class CommandCreatForm(forms.ModelForm):
    class Meta:
        model = Command
        exclude = ("author",)
