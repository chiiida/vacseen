from rest_framework.test import force_authenticate, APIClient
from datetime import date
from django.test import TestCase, RequestFactory, Client
from django.http import QueryDict, JsonResponse
import requests

from users.forms import DateExpiredForm
from users.views import calculate_age, next_date
from vaccine.models import *
from vaccine.views import *


class VaccineViewsTest(TestCase):

    def setUp(self):
        self.request_factory = RequestFactory()
        self.client = APIClient()
        self.user = CustomUser.objects.create(username='peter@gmail.com',
                                              first_name='Peter',
                                              last_name='Park',
                                              contact='0878867888',
                                              emergency_contact='0867888757',
                                              gender='Male',
                                              birthdate='1996-05-19',)
        self.user.save()
        self.client.force_authenticate(user=self.user)
        self.vacc_model = VaccineModel.objects.create(vaccine_name='BCG',
                                                      required_age=0.0,
                                                      required_gender='None')
        self.vacc_model.save()
        self.dose_model = DoseModel.objects.create(vaccine=self.vacc_model,
                                                   dose_count=1,
                                                   dose_duration=0)
        self.dose_model.save()
        self.vaccine = Vaccine.objects.create(vaccine_name=self.vacc_model.vaccine_name,
                                              user=self.user)
        self.vaccine.save()
        self.dose = Dose.objects.create(vaccine=self.vaccine,
                                        dose_count=1,
                                        dose_duration=0,
                                        received=False)
        self.dose.save()

    def test_track_first_date(self):
        url = reverse('vaccine:trackfirstdate', args=[self.vaccine.id, ])
        ordinary_dict = {'expired_month': ['12'], 'expired_day': [
            '3'], 'expired_year': ['2019']}
        data = QueryDict('', mutable=True)
        data.update(ordinary_dict)
        response = self.client.post(url, data=ordinary_dict)
        self.dose.refresh_from_db()
        self.dose.save()
        self.assertFalse(self.dose.received)
        expected_url = f'/?next=/vaccine/{self.dose.id}/'
        self.assertEqual(expected_url, response.url)

    def test_received_dose(self):
        url = reverse('vaccine:received', args=[self.dose.id,])
        response = self.client.post(url, data={'received-btn': '✔',})
        self.dose.refresh_from_db()
        expected_url = f'/?next=/vaccine/received/dose/{self.dose.id}/'
        self.assertEqual(response.status_code, 302)
        self.assertEqual(expected_url, response.url)
    
    def test_add_vaccine(self):
        url = reverse('vaccine:addvaccine')
        ordinary_dict = {'form-TOTAL_FORMS': ['1'],
                         'form-INITIAL_FORMS': ['0'],
                         'form-MIN_NUM_FORMS': ['0'],
                         'form-MAX_NUM_FORMS': ['1000'],
                         'form-0-vaccine_name': ['OPV'],
                         'form-0-dose_count': ['1'],
                         'form-0-date_taken_month': ['12'],
                         'form-0-date_taken_day': ['3'],
                         'form-0-date_taken_year': ['2019']}
        response = self.client.post(url, data=ordinary_dict, format="json")
        self.user.refresh_from_db()
        user_vaccine_list = [
            v.vaccine_name for v in self.user.vaccine_set.all()]
        print((response.request))
        # print(dir(response.client.post))
        print(response.data)
        print(user_vaccine_list)
        self.assertEqual(response.status_code, 302)
        self.assertEqual('/?next=/vaccine/add/', response.url)
        # self.assertTrue('OPV' in user_vaccine_list)
