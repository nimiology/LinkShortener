from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from LinkShortener.models import URL
from .forms import *
from .models import USER


def CREATEUSER(request):
    if not request.user.is_authenticated:
        FORMS = CreateUser(request.POST or None)
        context = {
            'FORMS': FORMS
        }

        if FORMS.is_valid():
            DATA = FORMS.cleaned_data
            user = USER(NAME=DATA['NAME'], USERNAME=DATA['USERNAME'],
                        EMAIL=DATA['EMAIL'], PASSWORD=DATA['PASSWORD1'],
                        Change=False)
            user.save()
            context['STATUS'] = 'Created!'
            return redirect(reverse('Dashboard:Signin'))

        return render(request, 'Dashboard/Sample.html', context)

    return redirect('/Dashboard')


def LOGIN(request):
    if not request.user.is_authenticated:
        FORM = Login(request.POST or None)
        context = {
            'FORMS': FORM
        }
        if FORM.is_valid():
            DATA = FORM.cleaned_data
            qs = USER.objects.filter(EMAIL__exact=DATA['EMAIL'])
            if qs.exists():
                user = authenticate(username=qs.values()[0]['USERNAME'], password=DATA['PASSWORD'])
                if user is not None:
                    login(request, user)
            else:
                context['STATUS'] = 'Check username and password!'

        return render(request, 'Dashboard/Sample.html', context)
    return redirect('/Dashboard')


def LOGOUT(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect(reverse('Dashboard:Signin'))


def CREATELINK(request):
    if request.user.is_authenticated:
        FORM = CreateLink(request.POST or None)
        context = {
            'FORMS' : FORM
        }

        if FORM.is_valid():
            DATA = FORM.cleaned_data
            url = URL(Title=DATA['Title'],Link=DATA['Link'],Owner=USER.objects.get(USERNAME=request.user.username))
            url.save()
            context['STATUS'] = url.Slug
        return render(request,'Dashboard/Sample.html',context)
    return redirect(reverse('Dashboard:Signin'))


def DELETELINK(request,Slug):
    if request.user.is_authenticated:
        url = URL.objects.filter(Slug__exact=Slug,Owner__exact=USER.objects.get(USERNAME=request.user.username))
        if url.exists():
            url[0].delete()
            return redirect('/Dashboard')
        else:
            return render(request,'Dashboard/notfound.html')

    return redirect(reverse('Dashboard:Signin'))


def FORGOTPASSWORD(request,Slug):
    FORM = ForgetPassword(request.POST or None)
    context = {
        'FORMS' : FORM
    }
    if FORM.is_valid():
        DATA = FORM.cleaned_data
        user = USER.objects.get(PasswordForget=Slug)
        user.PASSWORD = DATA['PASSWORD1']
        user.save()
        return redirect(reverse('Dashboard:Signin'))

    return render(request,'Dashboard/Sample.html',context)


def EDITUSER(request):
    if request.user.is_authenticated:
        user = USER.objects.get(USERNAME=request.user.username)
        class FORM(forms.Form):
            NAME = forms.CharField(widget=forms.TextInput(attrs={'value':user.NAME}))
            USERNAME = forms.CharField(widget=forms.TextInput(attrs={'value':user.USERNAME}))
            PASSWORD = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'value':user.PASSWORD}))

            def clean_USERNAME(self):
                USERNAME = self.cleaned_data['USERNAME']
                qs = User.objects.filter(username__exact=USERNAME)
                print(qs)
                qs = list(qs)
                qs2 = USER.objects.get(USERNAME=request.user.username)
                if qs2 in qs:
                    qs.remove(qs2)
                if len(qs) != 0:
                    raise forms.ValidationError('username is already taken')
                return USERNAME

        FORM = FORM(request.POST or None)
        context = {
            'FORMS':FORM
        }
        if FORM.is_valid():
            DATA = FORM.cleaned_data
            user.USERNAME = DATA['USERNAME']
            user.NAME = DATA['NAME']
            user.PASSWORD = DATA['PASSWORD']
            user.save()
            context['STATUS'] = 'Changed!'
            logout(request)
            return redirect(reverse('Dashboard:Signin'))

        return render(request,'Dashboard/Sample.html',context)
    return redirect(reverse('Dashboard:Signin'))


def EDITLINK(request,Slug):
    if request.user.is_authenticated:
        link = URL.objects.get(Slug=Slug,Owner__USERNAME__exact=request.user.username)
        class CreateLink(forms.Form):
            Title = forms.CharField(widget=forms.TextInput,initial=link.Title)
            Link = forms.CharField(widget=forms.TextInput, initial=link.Link)
            def clean_Link(self):
                LINK = self.cleaned_data['Link']
                if not 'https://' in LINK or 'http://' in LINK:
                    raise forms.ValidationError('This is not a link!')
                return LINK

        FORM = CreateLink(request.POST or None)
        context = {
            'FORMS' : FORM,
            'LINK' : link
        }

        if FORM.is_valid():
            DATA = FORM.cleaned_data
            link.Title = DATA['Title']
            link.Link = DATA['Link']
            link.save()
        context['URL'] = request.get_host()+'/'+link.Slug
        return render(request,'Dashboard/URL.html',context)
    return redirect(reverse('Dashboard:Signin'))


def ALLUSERLINKS(request):
    if request.user.is_authenticated:
        LINKS = URL.objects.filter(Owner__USERNAME__exact=request.user.username)
        if LINKS.exists():
            return render(request,'Dashboard/URLS.html',{'LINKS':LINKS})
        return render(request,'Dashboard/notfound.html')
    return redirect(reverse('Dashboard:Signin'))