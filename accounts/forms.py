from datetime import date

from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Clients
from django.db import models
from django import forms

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ('username', 'password', 'email')
        widgets = {
            'password': forms.PasswordInput()
        }


def aauthenticate(request, username, password):
    pass


def set_password(password):
    pass


class MyLoginForm(forms.Form):
    login = forms.CharField(max_length=30, )
    password = forms.CharField(max_length=30, )
    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super(MyLoginForm, self).__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        username = cleaned_data.get("login")
        password = cleaned_data.get("password")

        if username and password:
            self.user = authenticate(self.request, username=username, password=password)
            if self.user is None:
                print('Неверное имя пользователя или пароль')
                raise forms.ValidationError("Неверное имя пользователя или пароль.")
            else:
                print(f'Пользователь:{username} успешно авторизован!')
        return cleaned_data

    def get_user(self):
        return self.user


