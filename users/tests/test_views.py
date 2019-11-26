from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect

from users.models import CustomUser
from users.forms import CustomUserForm
import datetime

from django.test import TestCase, RequestFactory, Client
from rest_framework.test import force_authenticate, APIClient
from users.views import *


class ProfileViewTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create(first_name='User A')
        self.user.save()
        self.request_factory = RequestFactory()
        self.request = self.request_factory.get('/users/profile/2/')
        self.request.user = self.user
        self.client = APIClient()
        self.response = user_view(self.request, user_id=1)

    def test_index(self):
        response = self.client.get(path='')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_signup(self):
        response = self.client.get(path='/users/signup/')
        status = response.status_code
        self.assertEqual(status, 200)

    # def test_user_view_without_login(self):
    #     # self.assertTrue(200, self.response.status_code)
    #     self.response.client = Client()
    #     self.assertTemplateUsed(self.response, 'index.html')

    def test_user_view(self):
        self.client.force_authenticate(user=self.user)
        # self.assertTrue(200, self.response.status_code)
        self.assertContains(self.response, self.user.first_name)
