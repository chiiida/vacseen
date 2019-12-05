from django.test import TestCase

from users.models import CustomUser
from vaccine.models import Vaccine
from vaccine.models import Dose as UserDose

class VaccineTest(TestCase):

    def setUp(self):
        """Set up for testing"""
        self.user = CustomUser(first_name='User A')
        self.vac = Vaccine(vaccine_name="Hepatitis A",
                           required_age=10,
                           user=self.user)

    def test_string_representation(self):
        """Test string representation of Vaccine class."""
        self.assertEqual(
            str(self.vac), f"{self.vac.user.first_name}: {self.vac.vaccine_name}")

    def test_required_age(self):
        """Test required age"""
        self.assertEqual(10, self.vac.required_age)


class DoseTest(TestCase):

    def setUp(self):
        """Set up for testing"""
        self.user = CustomUser(first_name='User A')
        self.user.save()
        self.vac = Vaccine(vaccine_name="Hepatitis A", user=self.user)
        self.vac.save()
        self.dose_one = UserDose(vaccine=self.vac, dose_count=1)
        self.dose_one.save()
        self.dose_two = UserDose(vaccine=self.vac, dose_count=2)
        self.dose_two.save()

    def test_string_representation(self):
        """Test string representation of Dose class."""
        self.assertEqual('User A: Hepatitis A: dose 1', str(self.dose_one))
        self.assertEqual('User A: Hepatitis A: dose 2', str(self.dose_two))

    def test_vaccine(self):
        """Test that Dose class have a foreign key as Vaccine class."""
        self.assertEqual(self.vac, self.dose_one.vaccine)
        self.assertEqual(self.vac, self.dose_two.vaccine)

    def test_receive_status(self):
        """Test received status of dose."""
        self.assertFalse(self.dose_one.received)
        self.assertFalse(self.dose_two.received)

    def test_not_last_dose(self):
        """Test dose is not a last dose."""
        self.assertTrue(self.dose_one.not_last_dose)
        self.assertFalse(self.dose_two.not_last_dose)
