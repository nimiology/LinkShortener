from django.urls import path
from .views import *


app_name = 'Dashboard'


urlpatterns = [
    path('signup',CREATEUSER,name='Signup'),
    path('signin',LOGIN,name='Signin'),
    path('logout',LOGOUT,name='Logout'),
    path('create',CREATELINK,name='Create'),
    path('delete/<Slug>',DELETELINK,name='Delete'),
    path('forgetpassword/<Slug>',FORGOTPASSWORD,name='ForgetPassword'),
    path('edit', EDITUSER, name='EditUser'),
    path('URLS', ALLUSERLINKS, name='ALLUSERLINKS'),
    path('URLS/<Slug>',EDITLINK,name='EditLink')

]