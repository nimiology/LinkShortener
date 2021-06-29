from django import forms
from .models import USER


class CreateUser(forms.Form):
    NAME = forms.CharField(widget=forms.TextInput)
    USERNAME = forms.CharField(widget=forms.TextInput)
    EMAIL = forms.EmailField(widget=forms.EmailInput)
    PASSWORD1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    PASSWORD2 = forms.CharField(label='Password Confrim', widget=forms.PasswordInput)

    def clean_USERNAME(self):
        USERNAME = self.cleaned_data['USERNAME']
        qs = USER.objects.filter(USERNAME=USERNAME)
        if qs.exists():
            raise forms.ValidationError('Username is already exists!')
        return USERNAME

    def clean_EMAIL(self):
        EMAIL = self.cleaned_data['EMAIL']
        qs = USER.objects.filter(EMAIL=EMAIL)
        if qs.exists():
            raise forms.ValidationError('Email is already exists!')
        return EMAIL

    def clean(self):
        DATA = self.cleaned_data
        if len(DATA['PASSWORD1']) < 8:
            raise forms.ValidationError("Password is to short!")
        if DATA['PASSWORD1'] != DATA['PASSWORD2']:
            raise forms.ValidationError("Password doesn't match!")
        return DATA


class Login(forms.Form):
    EMAIL = forms.EmailField(widget=forms.EmailInput)
    PASSWORD = forms.CharField(widget=forms.PasswordInput)


class ForgetPassword(forms.Form):
    PASSWORD1 = forms.CharField(label='Password',widget=forms.PasswordInput)
    PASSWORD2 = forms.CharField(label='Password Confrim',widget=forms.PasswordInput)

    def clean(self):
        DATA = self.cleaned_data
        if DATA['PASSWORD1'] != DATA['PASSWORD2']:
            raise forms.ValidationError("PASSWORD doesn't match1")
        if len(DATA['PASSWORD1']) < 8:
            raise forms.ValidationError("PASSWORD must be 8 letter at least!")

        return DATA


class CreateLink(forms.Form):
    Title = forms.CharField(widget=forms.TextInput)
    Link = forms.CharField(widget=forms.TextInput)

    def clean_Link(self):
        LINK = self.cleaned_data['Link']
        if not 'https://' in LINK or 'http://' in LINK:
            raise forms.ValidationError('This is not a link!')
        return LINK
