from django.test import TestCase

from users.models import CustomUser
from vaccine.models import *


class CustomUserTests(TestCase):

    def setUp(self):
        self.user = CustomUser(
            first_name='UserA', email='private@gmail.com')
        self.user.save()

    def test_string_representation(self):
        self.assertEqual('private@gmail.com', str(self.user))

    def test_update_user_info(self):
        self.user.update_profile(last_name='Lastname', gender='Male')
        self.assertEqual('Lastname', self.user.last_name)
        self.assertEqual('Male', self.user.gender)

    def test_sorted_vaccine_set(self):
        vaccine_one = Vaccine(vaccine_name='Hepatitis A',
                              user=self.user)
        vaccine_one.save()
        vaccine_two = Vaccine(vaccine_name='BCG',
                              user=self.user)
        vaccine_two.save()
        vaccine_three = Vaccine(vaccine_name='DTP-HB1',
                              user=self.user)
        vaccine_three.save()
        vaccines = list(self.user.sorted_vaccine())
        self.assertEqual('UserA: BCG', str(vaccines[0]))
        self.assertEqual(vaccine_one, vaccines[-1])
