from django.urls import path

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('loginhandler', views.LoginHandler, name='loginhandler')
]