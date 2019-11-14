from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from users.models import CustomUser
from users.forms import CustomUserForm
import datetime

from django.test import TestCase, Client
from users.views import signup, vaccination_signup

class ViewsTests(TestCase) :

    def test_index(self) :
        c = Client()
        response = c.get(path='')
        status = response.status_code
        self.assertEqual(status, 200)
    
    def test_signup(self) :
        c = Client()
        response = c.get(path='/users/signup/')
        status = response.status_code
        self.assertEqual(status, 200)

    # def test_profile(self) :
    #     c = Client()
    #     response = c.get(path='/users/profile/')
    #     status = response.status_code
    #     self.assertEqual(status, 200)