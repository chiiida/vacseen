from django import forms
from django.forms import formset_factory, modelformset_factory
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
from vaccine.models import VaccineModel, Vaccine, Dose
import datetime

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female')
]


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='First name', widget=forms.TextInput(
        attrs={'class': 'form-control-reg', 'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(
        attrs={'class': 'form-control-reg', 'placeholder': 'Enter Last Name'}))
    contact = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control-reg', 'placeholder': 'Enter Phone Number'}))
    emergency_contact = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control-reg', 'placeholder': 'Enter Phone Number'}))
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
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'contact',
                  'emergency_contact', 'gender', 'birthdate',)


class CustomUserForm(forms.Form):
    first_name = forms.CharField(label='First name', widget=forms.TextInput(
        attrs={'class': 'form-control-reg', 'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(
        attrs={'class': 'form-control-reg', 'placeholder': 'Enter Last Name'}))
    contact = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control-reg', 'placeholder': 'Enter Phone Number'}))
    emergency_contact = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control-reg', 'placeholder': 'Enter Phone Number'}))
    gender = forms.CharField(widget=forms.Select(choices=GENDER_CHOICES))
    birthdate = forms.DateField(widget=forms.SelectDateWidget(
        years=range(1940, 2020)), initial=datetime.date.today)

class VaccinationForm(forms.Form):
    vaccine_name = forms.CharField(label='Vac cine name', widget=forms.TextInput(
        attrs={'class': 'form-control-vacc vacc-name', 'placeholder': 'Vaccine name', 'list': 'vaccine'}))
    dose_count = forms.IntegerField(widget=forms.NumberInput(
        attrs={'class': 'form-control-vacc vacc-dose', 'placeholder': 'Dose count', 'max': '3', 'min': '1'}))
    expired = forms.DateField(widget=forms.SelectDateWidget(
        years=range(1940, 2020)), initial=datetime.date.today)

VaccineFormSet = formset_factory(VaccinationForm, extra=1)

