import datetime
from django.db import models
from django.contrib import admin 
from django.contrib.auth.models import User
from oauth2client.contrib.django_util.models import CredentialsField
from django.utils import timezone

class CredentialsModel(models.Model): 
    id = models.ForeignKey(User, primary_key = True, on_delete = models.CASCADE) 
    credential = CredentialsField() 
    task = models.CharField(max_length = 80, null = True) 
    updated_time = models.CharField(max_length = 80, null = True) 
  
  
class CredentialsAdmin(admin.ModelAdmin): 
    pass

class Vaccine(models.Model):
    vaccine_name = models.CharField(max_length=100)
     
    def __str__(self):
        return self.vaccine_name

class Dose(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    dose_count = models.IntegerField(default=1)
    dose_duration = models.IntegerField(default=0)

    def __str__(self):
        return f"{str(self.vaccine)} : dose {self.dose_count}" 
    