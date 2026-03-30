from django import forms

from computer.models import Computer
from event.models import Program


class ProgramCreateForm(forms.ModelForm):
    class Meta:
        model = Program
        exclude = ("user",)
        widgets = {
            'computers': forms.CheckboxSelectMultiple(),
        }

    def __init__(self, user=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if user:
            self.fields['computers'].queryset = Computer.objects.filter(users=user)
        else:
            self.fields['computers'].queryset = Computer.objects.none()
