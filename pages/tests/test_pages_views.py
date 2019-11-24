from django.test import TestCase, RequestFactory, Client
from users.models import CustomUser
from rest_framework.test import force_authenticate, APIClient
from pages.views import *


class PagesViewsTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.client = APIClient()
        self.user = CustomUser.objects.create(first_name='User A')
        self.user.save()

    def test_login_handler_without_signup(self):
        request = self.request_factory.get('/users/profile/')
        request.user = self.user
        self.client.force_authenticate(user=self.user)
        response = LoginHandler(request)
        response.client = self.client
        self.assertRedirects(
            response, '/users/signup/')

    def test_login_handler_already_signup(self):
        user = CustomUser.objects.create(username='User',
                                         first_name='User',
                                         last_name='A',
                                         contact='081764889',
                                         emergency_contact='0878274444',
                                         gender='Male',
                                         birthdate='1999-07-30')
        user.save()
        request = self.request_factory.get('/users/profile/')
        request.user = user
        self.client.force_authenticate(user=user)
        response = LoginHandler(request)
        response.client = Client()
        self.assertRedirects(
            response, '/users/profile/', target_status_code=302)

    def test_404_handler(self):
        response = self.client.get(path='/users/signup/beebooo')
        status = response.status_code
        self.assertEqual(status, 404)
        self.assertTemplateUsed(response, '404.html')
