from django.test import TestCase
from vaccine.models import VaccineModel, DoseModel


class VaccineModelTest(TestCase):

    def test_string_representation(self):
        """Test string representation of VaccineModel class."""
        vac = VaccineModel(vaccine_name="BCG")
        self.assertEqual(str(vac), 'Model: ' + vac.vaccine_name)

    def test_stimulate_phase(self):
        """Test stimulate phase"""
        vac = VaccineModel(vaccine_name="BCG", stimulate_phase=10)
        self.assertEqual(10, vac.stimulate_phase)


class DoseModelTest(TestCase):

    def test_string_representation(self):
        """Test string representation of DoseModel class."""
        vac = VaccineModel(vaccine_name="BCG")
        dose = DoseModel(vaccine=vac, dose_count=2)
        self.assertEqual(
            str(dose), f"{str(dose.vaccine)} : dose {dose.dose_count}")
        self.assertEqual(2, dose.dose_count)
