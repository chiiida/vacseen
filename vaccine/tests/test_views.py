from django.test import TestCase, RequestFactory, Client
from rest_framework.test import force_authenticate, APIClient

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
        self.vacc_model = VaccineModel(vaccine_name='BCG',
                                       required_age=0.0,
                                       required_gender='None')
        self.vacc_model.save()
        self.dose_model = DoseModel(vaccine=self.vacc_model,
                                    dose_count=1,
                                    dose_duration=0)
        self.dose_model.save()
        self.vaccine = Vaccine(vaccine_name=self.vacc_model.vaccine_name,
                               user=self.user)
        self.vaccine.save()
        self.dose = Dose(vaccine=self.vaccine,
                         dose_count=1,
                         dose_duration=0,
                         received=False)
        self.dose.save()

    def test_track_first_date(self):
        request = self.request_factory.get(
            reverse('users:profile', args=(self.user.id,)))
        request.user = self.user
        self.client.force_authenticate(user=self.user)
        data = {'expired': "2019-12-01"}
        # form = DateExpiredForm(data={'expired': "2019-12-01"})
        track_first_date(request, vaccine_id=self.vaccine.id)
        response = self.client.post(
            reverse('vaccine:trackfirstdate', args=(self.vaccine.id,)), data)
        self.assertEqual('2019-12-01', self.dose.date_expired)
        self.assertFalse(self.dose.received)
