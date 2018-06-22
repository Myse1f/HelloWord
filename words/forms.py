# coding:utf-8
from django import forms
from .models import Vocabulary
from django.contrib.auth.models import User
import re

class UserForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput())
    email = forms.EmailField(widget=forms.EmailInput())
    password1 = forms.CharField(min_length=6, max_length=50, widget=forms.PasswordInput())
    password2 = forms.CharField(min_length=6, max_length=50, widget=forms.PasswordInput())
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

    # validate if both password is the same
    def clean_password(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
            raise forms.ValidationError('The password is not the same!')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput())
    password = forms.CharField(max_length=50, widget=forms.PasswordInput())

class SettingsForm(forms.Form):
    daily_words = forms.IntegerField(min_value=1, max_value=1000)
    try:
        vocabularys = Vocabulary.objects.all()
        choices = tuple([(v.id, v.name) for v in vocabularys])
        vocabulary = forms.ChoiceField(choices=choices, widget=forms.widgets.Select())
    except:
        choices = (1, 1)
        vocabulary = forms.ChoiceField(choices=choices, widget=forms.widgets.Select())

class NoteForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea)
    shared = forms.BooleanField(required=False, initial=True)
