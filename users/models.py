from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
    contact = models.CharField(max_length=30, blank=True, null=True)
    emergency_contact = models.CharField(max_length=30, blank=True, null=True)
    gender = models.BooleanField(default=True)
    birthdate = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return self.email


