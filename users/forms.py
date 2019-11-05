from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

GENDER_CHOICES = [
    ('M', 'Male'),
    ('F', 'Female')
]

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label='First name', widget=forms.TextInput(attrs={'class':'form-control-reg', 'placeholder': 'Enter First Name'}))
    last_name = forms.CharField(label='Last name', widget=forms.TextInput(attrs={'class':'form-control-reg', 'placeholder': 'Enter Last Name'}))
    contact = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control-reg', 'placeholder': 'Enter Phone Number'}))
    emergency_contact = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control-reg', 'placeholder': 'Enter Phone Number'}))
    gender = forms.CharField(widget=forms.Select(choices=GENDER_CHOICES))
    birthdate = forms.DateField(widget=forms.SelectDateWidget)

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'contact', 'emergency_contact', 'gender', 'birthdate',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        del self.fields['password1']
        del self.fields['password2']

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'contact', 'emergency_contact', 'gender', 'birthdate',)

