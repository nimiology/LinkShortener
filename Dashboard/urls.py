from django.urls import path
from .views import *

app_name = 'Dashboard'

urlpatterns = [
    path('signup/', sign_up_view, name='signup'),
    path('signin/', sign_in_view, name='signIn'),
    path('edit/', edit_user, name='editUser'),
    path('forgetpassword/<slug>/', forget_password, name='forgetPassword'),
    path('logout/', LOGOUT, name='logout'),

    path('url/create/', create_link, name='createLink'),
    path('url/<slug>/delete/', delete_link, name='deleteLink'),
    path('url/all/', user_links, name='links'),
    path('url/<slug>/edit/', edit_link, name='editLink')

]
