from django.urls import path
from .views import Direct

urlpatterns = [
    path('<slug>', Direct),
]
