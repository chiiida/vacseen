from django.test import TestCase

from users.models import CustomUser
from vaccine.models import VaccineModel, Vaccine, DoseModel
from vaccine.models import Dose as UserDose

class VaccineTest(TestCase):

    def setUp(self):
        self.user = CustomUser(first_name='User A')
        self.vac = Vaccine(vaccine_name="Hepatitis A",
                           required_age=10,
                           user=self.user)

    def test_string_representation(self):
        self.assertEqual(
            str(self.vac), f"{self.vac.user.first_name}: {self.vac.vaccine_name}")
    
    def test_required_age(self):
        self.assertEqual(10, self.vac.required_age)


class DoseTest(TestCase):

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

    def test_vaccine(self):
        self.assertEqual(self.vac, self.dose_one.vaccine)
        self.assertEqual(self.vac, self.dose_two.vaccine)

    def test_receive_status(self):
        self.assertFalse(self.dose_one.received)
        self.assertFalse(self.dose_two.received)
    
    def test_not_last_dose(self):
        self.assertTrue(self.dose_one.not_last_dose)
        self.assertFalse(self.dose_two.not_last_dose)
