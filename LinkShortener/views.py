from django.shortcuts import redirect, get_object_or_404
from .models import URL


def Direct(request, slug):
    link = get_object_or_404(URL, slug=slug)
    link.views += 1
    link.save()
    return redirect(link.link)
