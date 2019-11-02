from django.urls import path
from django.conf.urls import include, url
from django.conf import settings
# from django.contrib.auth.views import logout

from . import views

app_name = 'vacseenApp'
urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.index_page, name='login'),
    path('user/', views.user_page, name='user'),
    path('register/', views.register_page, name='register'),
    path('register/vacc/', views.register_vacc_page, name='regis-vacc'),
    url('gmailAuthenticate/', views.gmail_authenticate, name='gmail_authenticate'), 
    url('oauth2callback/', views.auth_return), 
]