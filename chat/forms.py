from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import TextInput


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields=['username','password1','password2']
        widgets = {
            'username': TextInput(attrs={'class':'form-control'}),
        }




from typing import Text
from django import forms
from django.forms import fields
from django.forms.widgets import Widget

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import transaction
#from importlib_metadata import email

from django.contrib.auth.forms import UserCreationForm

class Registration(UserCreationForm):
    email= forms.EmailField(required=True)
    class Meta:
        model= User
        fields=["email","password1","password2",]


