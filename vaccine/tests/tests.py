from django.test import TestCase

from vaccine.models import VaccineModel, Vaccine, DoseModel, Dose

class VaccineModelTest(TestCase):
    
    def test_string_representation(self):
        vac = VaccineModel(vaccine_name="BCG")
        self.assertEqual(str(vac),'Model: ' + vac.vaccine_name)


class VaccineTest(TestCase):
    
    def test_string_representation(self):
        user = CustomUser(first_name='User A')
        vac = Vaccine(vaccine_name="Hepatitis A", user=user)
        self.assertEqual(str(vac), f"{vac.user.first_name}: {vac.vaccine_name}")


class DoseModelTest(TestCase):

    def test_string_representation(self):
        vac = VaccineModel(vaccine_name="BCG")
        dose = DoseModel(vaccine=vac, dose_count=2)
        self.assertEqual(str(dose),f"{str(dose.vaccine)} : dose {dose.dose_count}" )

# class Dose(TestCase):

#     def test_string_representation(self):
#         vac = Vaccine(vaccine_name="Hepatitis A")
#         dose = Dose(vaccine=vac, dose_count=1)
#         self.assertEqual(str(dose),f"{str(dose.vaccine)} : dose {dose.dose_count}" )