from django.shortcuts import render, redirect
from django.contrib.auth import logout

from django.views.generic import TemplateView

class IndexPageView(TemplateView):
    template_name = 'vacseenApp/index.html'

def index_page(request):
    return render(request, 'vacseenApp/index.html')

def logout_user(request):
    """
    Function to logout user and redirect to index page. 
    """
    logout(request)
    return redirect('vacseenApp:index')

def register_page(request):
    stuff = 'aaaaaaÀ'
    context = {'stuff': stuff}
    return render(request, 'vacseenApp/regbasic.html', context)

def user_page(request):
    stuff = 'aaaaaaÀ'
    context = {'stuff': stuff}
    return render(request, 'vacseenApp/user.html', context)

def register_vacc_page(request):
    stuff = 'aaaaaaÀ'
    context = {'stuff': stuff}
    return render(request, 'vacseenApp/regvaccine.html', context)
