from django import forms

from models import Type


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
