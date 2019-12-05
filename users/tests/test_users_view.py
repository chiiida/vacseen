from django.shortcuts import reverse
from django.test import TestCase, Client
from rest_framework.test import APIClient

from users.models import CustomUser
from vaccine.models import VaccineModel, DoseModel


class SignedUpUserTest(TestCase):

    def setUp(self):
        """Setup fot testing"""
        self.user = CustomUser.objects.create(first_name='Testuser')
        self.user.save()
        self.signed_up_user = CustomUser.objects.create(username='User',
                                                        first_name='User',
                                                        last_name='A',
                                                        contact='081764889',
                                                        emergency_contact='0878274444',
                                                        gender='Male',
                                                        birthdate='1999-07-30')
        self.signed_up_user.save()
        self.vaccine = VaccineModel.objects.create(vaccine_name='OPV',
                                                   required_age=0,
                                                   required_gender='None')
        self.vaccine.save()
        self.dose = DoseModel.objects.create(vaccine=self.vaccine,
                                             dose_count=1,
                                             dose_duration=0)
        self.dose.save()
        self.apiclient = APIClient()
        self.apiclient.force_authenticate(user=self.signed_up_user)
        self.client = Client()
        self.client.force_login(user=self.signed_up_user)

    def test_index(self):
        """Test user get index page"""
        response = self.apiclient.get(path='')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_vaccination_signup_view(self):
        """Test user get vaccination page"""
        url = reverse('users:vaccination')
        response = self.apiclient.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vaccination')

    def test_post_vaccination(self):
        url = reverse('users:vaccination')
        ordinary_dict = {'form-TOTAL_FORMS': ['1'],
                         'form-INITIAL_FORMS': ['0'],
                         'form-MIN_NUM_FORMS': ['0'],
                         'form-MAX_NUM_FORMS': ['1000'],
                         'form-0-vaccine_name': ['OPV'],
                         'form-0-dose_count': ['1'],
                         'form-0-date_taken_month': ['12'],
                         'form-0-date_taken_day': ['3'],
                         'form-0-date_taken_year': ['2019']}
        response = self.client.post(url, data=ordinary_dict, follow=True)
        user_vaccine_list = [
            v.vaccine_name for v in self.signed_up_user.vaccine_set.all()]
        self.assertEqual(response.status_code, 200)
        self.assertTrue('OPV' in user_vaccine_list)

    def test_user_view(self):
        url = reverse('users:profile')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'User')


class NotSignupUserTest(TestCase):

    def setUp(self):
        """Setup fot testing"""
        self.user = CustomUser.objects.create(first_name='Testuser')
        self.user.save()
        self.vaccine = VaccineModel.objects.create(vaccine_name='OPV',
                                                   required_age=0,
                                                   required_gender='None')
        self.vaccine.save()
        self.dose = DoseModel.objects.create(vaccine=self.vaccine,
                                             dose_count=1,
                                             dose_duration=0)
        self.dose.save()
        self.client = Client()
        self.client.force_login(user=self.user)

    def test_signup(self):
        response = self.client.get(path='/users/signup/')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_post_signup_profile(self):
        url = reverse('users:vaccination')
        ordinary_dict = {'form-TOTAL_FORMS': ['1'],
                         'form-INITIAL_FORMS': ['0'],
                         'form-MIN_NUM_FORMS': ['0'],
                         'form-MAX_NUM_FORMS': ['1000'],
                         'first_name': ['Testuser'],
                         'last_name': ['Testuser'],
                         'contact': ['0888888888'],
                         'emergency_contact': ['191'],
                         'gender': ['Male'],
                         'birthdate_month': ['12'],
                         'birthdate_day': ['5'],
                         'birthdate_year': ['1996']}
        response = self.client.post(url, data=ordinary_dict)
        self.assertEqual(response.status_code, 302)
        # self.assertEqual('Male', self.user.gender)

    def test_user_view(self):
        url = reverse('users:profile')
        response = self.client.get(path=url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Testuser')
