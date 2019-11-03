from django.urls import path
from django.conf.urls import include, url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'vacseenApp'
urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('register/vacc/', views.register_vacc_page, name='regis-vacc'),
    path('', views.index_page, name='index'),
    path('user/', login_required(views.user_page), name='user'),
    url('gmailAuthenticate/', views.gmail_authenticate, name='gmail_authenticate'), 
    url('oauth2callback/', views.auth_return), 
]