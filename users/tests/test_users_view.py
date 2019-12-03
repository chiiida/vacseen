from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
import datetime
from django.test import TestCase, RequestFactory, Client
from rest_framework.test import force_authenticate, APIClient

from users.models import CustomUser
from users.forms import CustomUserForm
from vaccine.models import VaccineModel, DoseModel


class ProfileViewTest(TestCase):

    def setUp(self):
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
        self.client = APIClient()

        self.vaccine = VaccineModel.objects.create(vaccine_name='OPV',
                                                    required_age=0,
                                                    required_gender='None')
        self.vaccine.save()
        self.dose = DoseModel.objects.create(vaccine=self.vaccine,
                                             dose_count=1,
                                             dose_duration=0)
        self.dose.save()


    def test_index(self):
        response = self.client.get(path='')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_signup(self):
        response = self.client.get(path='/users/signup/')
        status = response.status_code
        self.assertEqual(status, 200)

    def test_vaccination_signup_view(self):
        self.client.force_authenticate(user=self.user)
        url = 'users:vaccination'
        response = self.client.get(path='/users/signup/vaccination', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Vaccination')
    
    def test_post_vaccination(self):
        self.client.force_authenticate(user=self.signed_up_user)
        ordinary_dict = {'form-TOTAL_FORMS': ['1'],
                         'form-INITIAL_FORMS': ['0'],
                         'form-MIN_NUM_FORMS': ['0'],
                         'form-MAX_NUM_FORMS': ['1000'],
                         'form-0-vaccine_name': ['OPV'],
                         'form-0-dose_count': ['1'],
                         'form-0-date_taken_month': ['12'],
                         'form-0-date_taken_day': ['3'],
                         'form-0-date_taken_year': ['2019']}
        # response = self.client.post(path='/users/signup/vaccination/',
        #                             data=ordinary_dict)
        # print(response)
        
    def test_user_view(self):
        self.client.force_authenticate(user=self.signed_up_user)
        url = reverse('users:profile', args=[self.signed_up_user.id, ])
        response = self.client.get(path=url, follow=True)
        expected_url = '/?next=/users/profile/2/'
        self.assertRedirects(response, expected_url)
        self.assertEqual(response.status_code, 200)
        # self.assertContains(response, self.user.first_name + ' ' + self.user.last_name)


