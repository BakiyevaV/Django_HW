from django.forms import ModelForm
from .models import Clients
from django.db import models
from django import forms

class UserForm(ModelForm):
    class Meta:
        model = Clients
        fields = ('login', 'password', 'email', 'birth_date')

class LoginForm(forms.Form):
    login = forms.CharField(max_length=30, )
    password = forms.CharField(max_length=30)
    class Meta:
        model = Clients
        fields = ('login', 'password')


