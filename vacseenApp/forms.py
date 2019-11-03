from django.contrib.auth.models import User
from .models import Vaccine, Dose
from django.forms import ModelForm, Textarea, TextInput
from django import forms

class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['firstname', 'lastname', 'phonenumber', 'gender', 'birthdate', 'imageUploadlabel']