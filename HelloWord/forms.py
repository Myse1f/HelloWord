# coding:utf-8
from django import forms
from .models import Vocabulary
from django.contrib.auth.models import User
import re

class UserForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(max_length=50, widget=forms.PasswordInput())
    password2 = forms.CharField(max_length=50, widget=forms.PasswordInput())
    daily_words = forms.IntegerField(min_value=1, max_value=1000, initial=50)
    try:
        vocabularys = Vocabulary.objects.all()
        choices = tuple([(v.id, v.name) for v in vocabularys])
        vocabulary = forms.ChoiceField(choices=choices, widget=forms.widgets.Select()) 
    except:
        choices = (1, 1)
        vocabulary = forms.ChoiceField(choices=choices, widget=forms.widgets.Select())
    
    # validate username
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^\w+$', username):
            raise forms.ValidationError('Username can only contain letter, number and _')
        try:
            User.objects.get(username = username)
        except User.DoesNotExist:
            return username