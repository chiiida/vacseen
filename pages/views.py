from django.shortcuts import render,redirect

# Create your views here.
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = 'home.html'

def LoginHandler(request):
    print(request.user.gender)
    if request.user.gender:
        return redirect('/users/')
    else:
        print('ekwai')
        return redirect('/users/signup')