from django import forms
from django.forms import formset_factory
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
import datetime

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female')
]


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='First name', widget=forms.TextInput(
        attrs={'class': 'form-control-reg',
               'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(
        attrs={'class': 'form-control-reg',
               'placeholder': 'Enter Last Name'}))
    contact = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control-reg',
               'placeholder': 'Enter Phone Number'}))
    emergency_contact = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control-reg',
               'placeholder': 'Enter Phone Number'}))
    gender = forms.CharField(widget=forms.Select(choices=GENDER_CHOICES))
    birthdate = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'contact',
                  'emergency_contact', 'gender', 'birthdate',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']


class CustomUserChangeForm(UserChangeForm):
    """User's profile change input form."""
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'contact',
                  'emergency_contact', 'gender', 'birthdate',)


class CustomUserForm(forms.Form):
    """User's profile input form."""
    first_name = forms.CharField(label='First name', widget=forms.TextInput(
        attrs={'class': 'form-control-reg',
               'placeholder': 'Enter First Name',
               'id': 'firstname'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(
        attrs={'class': 'form-control-reg',
               'placeholder': 'Enter Last Name'}))
    contact = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control-reg',
               'placeholder': 'Enter Phone Number'}))
    emergency_contact = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control-reg',
               'placeholder': 'Enter Phone Number'}))
    gender = forms.CharField(widget=forms.Select(choices=GENDER_CHOICES))
    birthdate = forms.DateField(widget=forms.SelectDateWidget(
        years=range(1940, 2020)), initial=datetime.date.today)


class VaccinationForm(forms.Form):
    """User's vaccination input form."""
    vaccine_name = forms.CharField(label='Vaccine name',
                                   widget=forms.TextInput(
                                       attrs={'class':
                                              'form-control-vacc vacc-name',
                                              'placeholder': 'Vaccine name',
                                              'id': 'vaccinename',
                                              'list': 'vaccine'}))
    dose_count = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control-vacc vacc-dose',
               'placeholder': 'Dose count', 'max': '3', 'min': '1'}))
    date_taken = forms.DateField(widget=forms.SelectDateWidget(
        years=range(1940, 2020)), initial=datetime.date.today)


class DateExpiredForm(forms.Form):
    """User's first date of vaccination input form."""
    date_taken = forms.DateField(widget=forms.SelectDateWidget(
        years=range(1940, 2020)), initial=datetime.date.today)


VaccineFormSet = formset_factory(VaccinationForm, extra=1)
