from django.test import TestCase, RequestFactory, Client
from rest_framework.test import APIClient

from users.models import CustomUser
from pages.views import LoginHandler, handler500
from vacseen import urls


class PagesViewsTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.client = APIClient()
        self.user = CustomUser.objects.create(first_name='User A')
        self.user.save()
        self.signed_up_user = CustomUser.objects.create(username='User',
                                                        first_name='User',
                                                        last_name='A',
                                                        contact='081764889',
                                                        emergency_contact='0878274444',
                                                        gender='Male',
                                                        birthdate='1999-07-30')
        self.signed_up_user.save()

    def test_render_index(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, 'Sign in with Google')

    def test_login_handler_without_signup(self):
        request = self.request_factory.get('/users/profile/')
        request.user = self.user
        self.client.force_authenticate(user=self.user)
        response = LoginHandler(request)
        response.client = self.client
        self.assertRedirects(
            response, '/users/signup/')

    def test_login_handler_already_signup(self):
        request = self.request_factory.get('/accout/login/')
        request.user = self.signed_up_user
        self.client.force_authenticate(user=self.signed_up_user)
        response = LoginHandler(request)
        response.client = self.client
        status = response.status_code
        self.assertEqual(status, 302)
        self.assertRedirects(
            response, '/users/profile/', target_status_code=302)

    def test_404_handler(self):
        response = self.client.get(path='/users/signup/beebooo')
        status = response.status_code
        self.assertEqual(status, 404)
        self.assertTemplateUsed(response, '404.html')
        self.assertTrue(urls.handler404.endswith('.handler404'))

    def test_500_handler(self):
        request = self.request_factory.get(path='/')
        response = handler500(request)
        response.client = Client()
        status = response.status_code
        self.assertEqual(status, 500)
        self.assertTrue(urls.handler500.endswith('.handler500'))
