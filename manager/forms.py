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
        exclude = ('created',)


class BasePointForm(forms.ModelForm):
    class Meta:
        model = Point
        exclude = ('created', 'post')


class PointForm(BasePointForm):
    photos = forms.FileField(label=u'Фотографии', required=False,
                             widget=forms.ClearableFileInput(attrs={'multiple':'true'}))
    description = forms.CharField(label=u'Краткое описание',
                                  required=False,
                                  max_length=256,
                                  widget=forms.Textarea(attrs={'style':'width:400px;'})
                                  )
    coordinates = forms.CharField(label=u'Координаты')



class UploadImageForm(forms.ModelForm):
    class Meta:
        model = EditorImage
        exclude = ('created',)

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('message', 'state')

class TransForm(forms.ModelForm):
    description = forms.CharField(label=u'Краткое описание',
                                  required=False,
                                  max_length=256,
                                  widget=forms.Textarea(attrs={'style':'width:400px;'}))

    class Meta:
        model = Translation
        fields = ('name', 'description', 'address')

    def __init__(self, *args, **kwargs):
        res = super(TransForm, self).__init__(*args, **kwargs)
        if self.instance.point is not None:
            self.initial['name'] = self.instance.name or self.instance.point.name
            self.initial['description'] = self.instance.description or self.instance.point.description
            self.initial['address'] = self.instance.address or self.instance.point.address            
        return res

class TransFormTrack(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ('name', 'description')

    
