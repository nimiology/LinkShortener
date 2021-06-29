from django.shortcuts import render, redirect,get_object_or_404
from .models import URL


def Direct(request,Slug):
    LINK = get_object_or_404(URL,Slug=Slug)
    LINK.Views += 1
    LINK.save()
    return redirect(LINK.Link)
