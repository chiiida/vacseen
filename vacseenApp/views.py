from django.shortcuts import render, redirect
from .models import CredentialsModel
from vacseensite import settings
import requests, httplib2
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.contrib.django_util.models import CredentialsField
from oauth2client.contrib import xsrfutil
from oauth2client.client import flow_from_clientsecrets
from apiclient.discovery import build
from django.contrib.auth import logout

FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/gmail.readonly',
    redirect_uri='http://127.0.0.1:8000/oauth2callback',
    prompt='consent')

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

def gmail_authenticate(request): 
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user.id, 'credential') 
    credential = storage.get() 
    login_user(request)
  
    if credential is None or credential.invalid: 
        FLOW.params['state'] = xsrfutil.generate_token(settings.SECRET_KEY, 
                                                              request.user) 
        authorize_url = FLOW.step1_get_authorize_url() 
        return HttpResponseRedirect(authorize_url) 
    else: 
        http = httplib2.Http() 
        http = credential.authorize(http) 
        service = build('gmail', 'v1', http = http) 
        print('access_token = ', credential.access_token) 
        status = True
        return render(request, 'vacseenApp/user.html', {'status': status})

def auth_return(request): 
    get_state = bytes(request.GET.get('state'), 'utf8') 
    if not xsrfutil.validate_token(settings.SECRET_KEY, get_state, 
                                   request.user): 
        return HttpResponseBadRequest() 
  
    credential = FLOW.step2_exchange(request.GET.get('code')) 
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user.id, 'credential') 
    storage.put(credential) 
  
    print("access_token: % s" % credential.access_token) 
    return HttpResponseRedirect("/")

def login_user(request): 
    status = True

    if not request.user.is_authenticated: 
        return render(request, 'vacseenApp/regbasic.html')
  
    storage = DjangoORMStorage(CredentialsModel, 'id', request.user.id, 'credential') 
    credential = storage.get() 
  
    try: 
        access_token = credential.access_token 
        resp, cont = Http().request("https://www.googleapis.com/auth/gmail.readonly", 
                                     headers ={'Host': 'www.googleapis.com', 
                                             'Authorization': access_token}) 
    except: 
        status = False
        print('Not Found') 
  
    return render(request, 'vacseenApp/user.html', {'status': status})