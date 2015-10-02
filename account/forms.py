# -*- coding: utf-8 -*-

from django import forms
from account.models import User


class UserCreationForm(forms.ModelForm):
    # password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    # password2 = forms.CharField(label='Повторить пароль', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'gender', 'email', 'bike', 'phone', 'address')

    # def clean_password2(self):
    #     password1 = self.cleaned_data.get("password1")
    #     password2 = self.cleaned_data.get("password2")
    #     if password1 and password2 and password1 != password2:
    #         raise forms.ValidationError("Пароли не совпадают!")
    #     return password2

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        # user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'bike', 'avatar')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'gender', 'email', 'phone', 'address')
