import datetime

from django.db import models
from django.utils import timezone

class User(models.Model):
    user_name = models.CharField(max_length=30)
    user_surname = models.CharField(max_length=30)
    user_gender = models.BooleanField(default=True)
    user_tel = models.CharField(max_length=10)
    user_birthday = models.DateField()
    user_contact = models.CharField(max_length=30, default='')
    user_emer_contact = models.CharField(max_length=30)
    user_vaccines = []

    def __str__(self):
        return self.user_name + ' ' + self.user_surname 

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
    