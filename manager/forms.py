# -*- coding: utf-8 -*-
from django import forms

from manager.models import Type, Track, Post, Point, EditorImage


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

class PointForm(forms.ModelForm):

    class Meta:
        model = Point
        exclude = ('created', 'post')


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = EditorImage
        exclude = ('created',)
