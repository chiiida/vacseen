from django.urls import include, path
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

app_name = 'vacseenApp'
urlpatterns = [
    path('register/', views.register_page, name='register'),
    path('register/vacc/', views.register_vacc_page, name='regis-vacc'),
    path('', views.IndexPageView.as_view(), name='index'),
    path('user/', (views.user_page), name='user'),
    # url('gmailAuthenticate/', views.gmail_authenticate, name='gmail_authenticate'), 
    # url('oauth2callback/', views.auth_return), 
]