from django.test import TestCase, RequestFactory, Client
from rest_framework.test import force_authenticate, APIClient
from datetime import date
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
        url = reverse('vaccine:trackfirstdate', args=[self.vaccine.id,])
        response = self.client.post(url, data={'expired': date(2019, 12, 12)})
        self.dose.refresh_from_db()
        self.assertFalse(self.dose.received)
        # self.assertTrue(response.data['expired'])
        # self.assertEqual('2019-12-01', self.dose.date_taken)
    
    def test_received_dose(self):
        url = reverse('vaccine:received', args=[self.dose.id,])
        response = self.client.post(url, data={'status': True})
        # request = self.request_factory.get(url)
        # request.user = self.user
        # received_dose(request, self.dose.id)
        # print(response)
        # print(self.dose.received)
        self.dose.refresh_from_db()
        # print(self.dose.received)
        # self.assertTrue(response.data['status'])
