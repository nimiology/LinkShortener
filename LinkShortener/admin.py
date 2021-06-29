from django.contrib import admin
from .models import URL
# Register your models here.
class LinksAdmin(admin.ModelAdmin):
    list_display = ['Title','Slug','Views']
admin.site.register(URL,LinksAdmin)