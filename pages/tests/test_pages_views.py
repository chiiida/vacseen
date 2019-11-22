from django.test import TestCase, Client
from users.models import CustomUser
from rest_framework.test import force_authenticate, APIClient


class PagesViewsTest(TestCase):

    def setUp(self):
       self.client = APIClient()

    # def test_login_handler_without_signup(self):
    #     user = CustomUser(first_name='User A')
    #     self.client.force_authenticate(user=user)
    #     response = self.client.get(path='/users/profile/', follow=True)
    #     print(response)
    #     self.assertRedirects(response, '/users/signup', status_code=200,
    #                          target_status_code=200, fetch_redirect_response=True)

        # with self.settings(LOGIN_URL='home'):
        #     response = self.client.get('')
        #     self.assertRedirects(response, '/users/signup', status_code=200)

    def test_404_handler(self):
        response = self.client.get(path='/users/signup/beebooo')
        status = response.status_code
        self.assertEqual(status, 404)
        self.assertTemplateUsed(response, '404.html')
