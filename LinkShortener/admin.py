from django.contrib import admin
from .models import URL


class URLAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'views']


admin.site.register(URL, URLAdmin)
