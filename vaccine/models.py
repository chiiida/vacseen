from django.db import models
from users.models import CustomUser

class Vaccine(models.Model):
    """
    count age that less than one year as decimal
    ex. 1 month old = 0.1, 2 years 5 month old = 2.5
    """
    vaccine_name = models.CharField(max_length=100)
    required_age = models.FloatField(default=0.0)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.vaccine_name

class Dose(models.Model):
    vaccine = models.ForeignKey(Vaccine, on_delete=models.CASCADE)
    dose_count = models.IntegerField(default=1)
    dose_duration = models.IntegerField(default=0)

    def __str__(self):
        return f"{str(self.vaccine)} : dose {self.dose_count}" 
