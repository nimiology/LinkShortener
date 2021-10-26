from django import forms
from .models import User


class CreateUserForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput)
    email = forms.EmailField(widget=forms.EmailInput)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput)

    def clean_username(self):
        username = self.cleaned_data['username']
        qs = User.objects.filter(username=username)
        if qs.exists():
            raise forms.ValidationError('Username is already exists!')
        return username

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError('Email is already exists!')
        return email

    def clean(self):
        DATA = self.cleaned_data
        if len(DATA['password1']) < 8:
            raise forms.ValidationError("Password is to short!")
        if DATA['password2'] != DATA['password1']:
            raise forms.ValidationError("Password doesn't match!")
        return DATA


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)


class ForgetPasswordForm(forms.Form):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password Confirm', widget=forms.PasswordInput)

    def clean(self):
        DATA = self.cleaned_data
        if len(DATA['password1']) < 8:
            raise forms.ValidationError("Password is to short!")
        if DATA['password2'] != DATA['password1']:
            raise forms.ValidationError("Password doesn't match!")
        return DATA


class URLForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput)
    link = forms.URLField(widget=forms.URLInput)
