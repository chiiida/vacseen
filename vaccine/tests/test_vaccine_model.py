from django.test import TestCase

from users.models import CustomUser
from vaccine.models import VaccineModel, Vaccine, DoseModel, Dose

class VaccineModelTest(TestCase):
    
    def test_string_representation(self):
        vac = VaccineModel(vaccine_name="BCG")
        self.assertEqual(str(vac),'Model: ' + vac.vaccine_name)


class DoseModelTest(TestCase):

    def test_string_representation(self):
        vac = VaccineModel(vaccine_name="BCG")
        dose = DoseModel(vaccine=vac, dose_count=2)
        self.assertEqual(str(dose),f"{str(dose.vaccine)} : dose {dose.dose_count}" )
