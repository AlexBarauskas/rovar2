# -*- coding: utf-8 -*-
from django import forms

from models import Type, Track


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type


class TrackForm(forms.ModelForm):
    xml_coordinates = forms.FileField(label='GPS Log', required=False)

    class Meta:
        model = Track
        exclude = ('created', 'post', 'coordinates')
