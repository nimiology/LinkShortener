from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib.auth import authenticate,login,logout
from .forms import *
from .models import USER
# Create your views here.

def CREATEUSER(request):
    if not request.user.is_authenticated:
        FORMS = CreateUser(request.POST or None)
        context = {
            'FORMS': FORMS
        }

        if FORMS.is_valid():
            DATA = FORMS.cleaned_data
            user = USER(NAME=DATA['NAME'],USERNAME=DATA['USERNAME'],
                     EMAIL=DATA['EMAIL'],PASSWORD=DATA['PASSWORD1'],
                     Change=False)
            user.save()
            context['STATUS'] = 'Created!'

        return render(request,'Dashboard/Sample.html',context)

    return redirect(reverse('Dashboard:Signin'))


def LOGIN(request):
    if not request.user.is_authenticated:
        FORM = Login(request.POST or None)
        context = {
            'FORMS' : FORM
        }
        if FORM.is_valid():
            DATA = FORM.cleaned_data
            qs = USER.objects.filter(EMAIL__exact=DATA['EMAIL'])
            if qs.exists():
                user = authenticate(username=qs.values()[0]['USERNAME'],password=DATA['PASSWORD'])
                if user is not None:
                    login(request,user)
            else:
                context['STATUS'] = 'Check username and password!'

        return render(request,'Dashboard/Sample.html',context)
    return redirect('/Dashboard')


def LOGOUT(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect(reverse('Dashboard:Signin'))