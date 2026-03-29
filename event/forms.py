from django import forms
from event.models import Program


class ProgramCreatForm(forms.ModelForm):
    class Meta:
        model = Program
        exclude = ("user",)
