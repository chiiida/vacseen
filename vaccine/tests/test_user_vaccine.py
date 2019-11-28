from django.test import TestCase

from users.models import CustomUser
from vaccine.models import VaccineModel, Vaccine, DoseModel
from vaccine.models import Dose as UserDose

class VaccineTest(TestCase):

    def test_string_representation(self):
        user = CustomUser(first_name='User A')
        vac = Vaccine(vaccine_name="Hepatitis A", user=user)
        self.assertEqual(
            str(vac), f"{vac.user.first_name}: {vac.vaccine_name}")

class Dose(TestCase):

    def setUp(self):
        self.user = CustomUser(first_name='User A')
        self.user.save()
        self.vac = Vaccine(vaccine_name="Hepatitis A", user=self.user)
        self.vac.save()
        self.dose_one = UserDose(vaccine=self.vac, dose_count=1)
        self.dose_one.save()
        self.dose_two = UserDose(vaccine=self.vac, dose_count=2)
        self.dose_two.save()

    def test_string_representation(self):
        self.assertEqual('User A: Hepatitis A: dose 1', str(self.dose_one))
        self.assertEqual('User A: Hepatitis A: dose 2', str(self.dose_two))
    
    def test_not_last_dose(self):
        self.assertTrue(self.dose_one.not_last_dose)
        self.assertFalse(self.dose_two.not_last_dose)
