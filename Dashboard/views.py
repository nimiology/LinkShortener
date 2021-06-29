from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout

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

