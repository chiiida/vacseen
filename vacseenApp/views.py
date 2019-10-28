from django.shortcuts import render, redirect
from django.contrib.auth import logout

# TODO all

def index_page(req):
    return render(req, 'vacseenApp/index.html')

def logout_page(req):
    logout(req)
    return redirect('vacseenApp:index')

def registerPage(req):
    stuff = 'aaaaaaÀ'
    context = {'stuff': stuff}
    return render(req, 'vacseenApp/index.html', context)

def userPage(req):
    stuff = 'aaaaaaÀ'
    context = {'stuff': stuff}
    return render(req, 'vacseenApp/index.html', context)