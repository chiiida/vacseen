from django.test import TestCase
from django import forms
from users.models import CustomUser
from vaccine.models import VaccineModel, DoseModel, Vaccine, Dose
from users.forms import *


class FormsTest(TestCase):

    def setup(self):
        user = CustomUser.objects.create(first_name='User', last_name='User')

    def test_valid_custom_user_form(self):
        """Test the valid user form."""
        form = CustomUserForm(
            data={
                'first_name': "firstname",
                'last_name': "lastname",
                'contact': "0823456789",
                'emergency_contact': "191",
                'gender': 'Male',
                'birthdate': "1999-07-30"
            })
        self.assertTrue(form.is_valid())

    def test_invalid_custom_user_form(self):
        """Test the invalid user form."""
        form = CustomUserForm(
            data={
                'first_name': "firstname",
                'last_name': "lastname",
                'contact': "0823456789",
                'emergency_contact': "",
                'gender': 'Male',
                'birthdate': ""
            })
        self.assertFalse(form.is_valid())

    def test_valid_vaccination_form(self):
        """Test the valid vaccination form."""
        form = VaccinationForm(
            data={
                'vaccine_name': "Hepatitis A",
                'dose_count': "1",
                'expired': "2019-01-01"
            })
        self.assertTrue(form.is_valid())

    def test_valid_vaccination_form(self):
        """Test the invalid vaccination form."""
        form = VaccinationForm(
            data={
                'vaccine_name': "Hepatitis A",
                'dose_count': "",
                'expired': ""
            })
        self.assertFalse(form.is_valid())

    def test_valid_vaccine_form_set(self):
        """Test the valid vaccination form set."""
        formset = VaccineFormSet(
            data={
                'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '1',
                'form-0-vaccine_name': "Hepatitis A",
                'form-0-dose_count': "1",
                'form-0-expired': "2019-01-01",
                'form-1-vaccine_name': "BCG",
                'form-1-dose_count': "1",
                'form-1-expired': "2019-05-01"
            })
        self.assertTrue(formset.is_valid())

    def test_invalid_vaccine_form_set(self):
        """Test the invalid vaccination form set."""
        formset = VaccineFormSet(
            data={
                'form-TOTAL_FORMS': '2',
                'form-INITIAL_FORMS': '1',
                'form-0-vaccine_name': "Hepatitis A",
                'form-0-dose_count': "1",
                'form-0-expired': "2019-01-01",
                'form-1-vaccine_name': "",
                'form-1-dose_count': "1",
                'form-1-expired': ""
            })
        self.assertFalse(formset.is_valid())
