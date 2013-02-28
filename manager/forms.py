from django import forms

from models import Type, Track


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type

class TrackForm(forms.ModelForm):
    class Meta:
        model = Track
        exclude = ('created', 'post')
