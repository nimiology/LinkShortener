from django import forms
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User

from LinkShortener.models import URL
from .forms import CreateUserForm, LoginForm, URLForm, ForgetPasswordForm
from .models import ForgetPassword


def sign_up_view(request):
    if not request.user.is_authenticated:
        form = CreateUserForm(request.POST or None)
        context = {
            'form': form
        }

        if form.is_valid():
            data = form.cleaned_data
            user = get_user_model()
            user.objects.create_user(username=data['username'], email=data['email'],
                                     password=data['password1'])
            context['status'] = 'Created!'
            return redirect(reverse('Dashboard:signIn'))

        return render(request, 'Dashboard/Sample.html', context)

    return redirect(reverse('Dashboard:links'))


def sign_in_view(request):
    if not request.user.is_authenticated:
        form = LoginForm(request.POST or None)
        context = {
            'form': form
        }
        if form.is_valid():
            data = form.cleaned_data
            try:
                qs = User.objects.get(email=data['email'])
                user = authenticate(username=qs.username, password=data['password'])
                if user is not None:
                    login(request, user)
                    return redirect(reverse('Dashboard:links'))
            except User.DoesNotExist:
                context['status'] = 'Check username and password!'

        return render(request, 'Dashboard/Sample.html', context)
    return redirect(reverse('Dashboard:links'))


def LOGOUT(request):
    if request.user.is_authenticated:
        logout(request)

    return redirect(reverse('Dashboard:signIn'))


def create_link(request):
    if request.user.is_authenticated:
        form = URLForm(request.POST or None)
        context = {
            'form': form
        }

        if form.is_valid():
            DATA = form.cleaned_data
            url = URL(title=DATA['title'], link=DATA['link'],
                      owner=User.objects.get(username=request.user.username))
            url.save()
            context['status'] = url.slug
        return render(request, 'Dashboard/Sample.html', context)
    return redirect(reverse('Dashboard:SignIn'))


def delete_link(request, slug):
    if request.user.is_authenticated:
        url = get_object_or_404(URL, slug=slug, owner__username=request.user.username)
        url.delete()
        return redirect(reverse('Dashboard:createLink'))

    return redirect(reverse('Dashboard:SignIn'))


def forget_password(request, slug):
    form = ForgetPasswordForm(request.POST or None)
    context = {
        'form': form
    }
    if form.is_valid():
        DATA = form.cleaned_data
        user = get_object_or_404(User, forgetPassword__slug=slug)
        user.set_password(DATA['password1'])
        user.save()
        logout(request)
        return redirect(reverse('Dashboard:signIn'))

    return render(request, 'Dashboard/Sample.html', context)


def edit_user(request):
    if request.user.is_authenticated:
        user = User.objects.get(username=request.user.username)

        class formCLS(forms.Form):
            username = forms.CharField(widget=forms.TextInput(attrs={'value': user.username}))
            password = forms.CharField(label='Password', widget=forms.PasswordInput())

            def clean_USERNAME(self):
                username = self.cleaned_data['username']
                qs = User.objects.filter(username=username)
                if qs.exists():
                    raise forms.ValidationError('username is already taken')
                return username

        form = formCLS(request.POST or None)
        context = {
            'form': form
        }
        if form.is_valid():
            DATA = form.cleaned_data
            user.USERNAME = DATA['username']
            user.set_password(DATA['password'])
            user.save()
            context['STATUS'] = 'Changed!'
            logout(request)
            return redirect(reverse('Dashboard:signIn'))

        return render(request, 'Dashboard/Sample.html', context)
    return redirect(reverse('Dashboard:signIn'))


def edit_link(request, slug):
    if request.user.is_authenticated:
        link_object = get_object_or_404(URL, slug=slug, owner__username=request.user.username)

        class CreateLink(forms.Form):
            title = forms.CharField(widget=forms.TextInput, initial=link_object.title)

        form = CreateLink(request.POST or None)
        context = {
            'form': form,
            'link': link_object
        }

        if form.is_valid():
            DATA = form.cleaned_data
            link_object.title = DATA['title']
            link_object.save()
        context['url'] = request.get_host() + '/' + link_object.slug
        return render(request, 'Dashboard/URL.html', context)
    return redirect(reverse('Dashboard:signIn'))


def user_links(request):
    if request.user.is_authenticated:
        LINKS = URL.objects.filter(owner__username=request.user.username)
        return render(request, 'Dashboard/URLS.html', {'LINKS': LINKS})
    return redirect(reverse('SignIn'))
