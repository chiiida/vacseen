from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView, name='home'),
    path('loginhandler', views.LoginHandler, name='loginhandler')
]
