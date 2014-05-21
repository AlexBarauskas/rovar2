# -*- coding: utf-8 -*-
from django import forms

from map.models import Type, Point, Track, Translation
from api.models import Message
from manager.models import EditorImage
from blog.models import Post


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type


class TrackForm(forms.ModelForm):
    xml_coordinates = forms.FileField(label='GPS Log', required=False)

    class Meta:
        model = Track
        exclude = ('created', 'post', 'coordinates', 'uid')

class PostForm(forms.ModelForm):
    text = forms.CharField(label="",required=True,
                           widget=forms.Textarea(attrs={'class':'tiny-editor'}))
    
    class Meta:
        model = Post
        exclude = ('created')


class BasePointForm(forms.ModelForm):
    class Meta:
        model = Point
        exclude = ('created', 'post', 'uid')


class PointForm(BasePointForm):
    photos = forms.FileField(label=u'Фотографии', required=False,
                             widget=forms.ClearableFileInput(attrs={'multiple':'true'}))




class UploadImageForm(forms.ModelForm):
    class Meta:
        model = EditorImage
        exclude = ('created',)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('message', 'state')

class TransForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ('name', 'description', 'address')
    
    
