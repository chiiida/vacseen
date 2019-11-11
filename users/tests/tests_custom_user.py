from django.test import TestCase

from users.models import CustomUser

class CustomUserTests(TestCase):

    def test_update_user_info(self):
        user = CustomUser()
        user.update_profile(first_name='UserA', gender='Male')
        self.assertEqual('UserA', user.first_name)
        self.assertEqual('Male', user.gender)
