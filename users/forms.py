from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='Firstname', widget=forms.TextInput(attrs={'placeholder': 'eiei'}))
    last_name = forms.CharField()
    contact = forms.CharField()
    emergency_contact = forms.CharField()
    gender = forms.BooleanField()
    birthdate = forms.DateField()

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'contact', 'emergency_contact', 'gender', 'birthdate',)

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'contact', 'emergency_contact', 'gender', 'birthdate',)

