from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.CharField(max_length=30)
    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    phonenumber = models.CharField(max_length=10)
    gender = models.BooleanField(default=True)
    birthdate = models.DateField()
    user_contact = models.CharField(max_length=30, default='')
    emer_contact = models.CharField(max_length=30)
    user_vaccines = []

    def __str__(self):
        return self.email