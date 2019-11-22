from django.test import TestCase, Client
from users.models import CustomUser
# from rest_framework.test import force_authenticate


class PagesViewsTest(TestCase):

    def setUp(self):
       self.client = Client()

    # def test_login_handler(self):
    #     request = factory.get('/users/signup/', follow=True)
    #     user = CustomUser.objects.get(id=1)
    #     force_authenticate(request, user=user, token=user.auth_token)

    def test_error_handler(self):
        response = self.client.get(path='/users/signup/beebooo')
        status = response.status_code
        self.assertEqual(status, 404)
        self.assertTemplateUsed(response, '404.html')
