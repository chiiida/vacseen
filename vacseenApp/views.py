from django.shortcuts import render, redirect
from django.contrib.auth import logout

# TODO all

def index_page(req):
    return render(req, 'vacseenApp/index.html')

def logout_page(req):
    logout(req)
    return redirect('vacseenApp:index')

def register_page(req):
    stuff = 'aaaaaaÀ'
    context = {'stuff': stuff}
    return render(req, 'vacseenApp/regbasic.html', context)

def user_page(req):
    stuff = 'aaaaaaÀ'
    context = {'stuff': stuff}
    return render(req, 'vacseenApp/user.html', context)

def register_vacc_page(req):
    stuff = 'aaaaaaÀ'
    context = {'stuff': stuff}
    return render(req, 'vacseenApp/regvaccine.html', context)