# -*- coding: utf-8 -*-
from django import forms

from models import Type, Track, Post


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type


class TrackForm(forms.ModelForm):
    xml_coordinates = forms.FileField(label='GPS Log', required=False)

    class Meta:
        model = Track
        exclude = ('created', 'post', 'coordinates')

class PostForm(forms.ModelForm):
    text = forms.CharField(label="",required=True,
                           widget=forms.Textarea(attrs={'class':'tiny-editor'}))
    
    class Meta:
        model = Post
        exclude = ('created')
