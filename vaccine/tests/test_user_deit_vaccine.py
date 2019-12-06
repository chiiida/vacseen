from django.test import TestCase, Client
from django.http import QueryDict
from django.urls import reverse

from users.models import CustomUser
from vaccine.models import VaccineModel, DoseModel, Vaccine, Dose


class UserEditVaccineTest(TestCase):

    def setUp(self):
        """Set up for testing"""
        self.user = CustomUser.objects.create(username='peter@gmail.com',
                                              first_name='Peter',
                                              last_name='Park',
                                              contact='0878867888',
                                              emergency_contact='0867888757',
                                              gender='Male',
                                              birthdate='1996-05-19',)
        self.user.save()
        self.vacc_model = VaccineModel.objects.create(vaccine_name='BCG',
                                                      required_age=0.0,
                                                      required_gender='None')
        self.vacc_model.save()
        self.vacc_model2 = VaccineModel.objects.create(vaccine_name='OPV',
                                                       required_age=0.0,
                                                       required_gender='None')
        self.vacc_model2.save()
        self.dose_model = DoseModel.objects.create(vaccine=self.vacc_model,
                                                   dose_count=1,
                                                   dose_duration=0)
        self.dose_model.save()
        name = self.vacc_model.vaccine_name
        self.vaccine = Vaccine.objects.create(vaccine_name=name,
                                              user=self.user)
        self.vaccine.save()
        self.dose = Dose.objects.create(vaccine=self.vaccine,
                                        dose_count=1,
                                        dose_duration=0,
                                        received=False)
        self.dose.save()
        self.client = Client()
        self.client.force_login(user=self.user)

    def test_track_first_date(self):
        """Test user add their first day of receive that vaccine."""
        url = reverse('vaccine:trackfirstdate', args=[self.vaccine.id, ])
        ordinary_dict = {'expired_month': ['12'],
                         'expired_day': ['3'],
                         'expired_year': ['2019'], }
        data = QueryDict('', mutable=True)
        data.update(ordinary_dict)
        response = self.client.post(url, data=ordinary_dict)
        self.dose.refresh_from_db()
        self.assertFalse(self.dose.received)
        # self.assertEqual('12-03-2019', self.dose.date_taken)
        self.assertEqual(response.status_code, 302)

    def test_received_dose(self):
        """Test user input that ther received that dose."""
        url = reverse('vaccine:received', args=[self.dose.id, ])
        response = self.client.post(url, data={'receivedbtn': ['received'], })
        expected_url = '/users/profile/'
        self.dose.refresh_from_db()
        self.assertTrue(self.dose.received)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(expected_url, response.url)

    def test_add_vaccine(self):
        """Test user add new vaccines."""
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
        response = self.client.post(url, data=ordinary_dict)
        user_vaccine_list = [
            v.vaccine_name for v in self.user.vaccine_set.all()]
        expected_url = '/users/profile/'
        self.assertEqual(expected_url, response.url)
        self.assertEqual(response.status_code, 302)
        self.assertTrue('OPV' in user_vaccine_list)

    def test_del_vaccine(self):
        """Test user remove a vaccine."""
        url = reverse('vaccine:delvaccine', args=[self.vaccine.id])
        response = self.client.post(url, data={'delvacc': ['1'], })
        self.assertEqual(response.status_code, 302)
        user_vaccine_list = [
            v.vaccine_name for v in self.user.vaccine_set.all()]
        self.assertTrue('BCG' not in user_vaccine_list)
