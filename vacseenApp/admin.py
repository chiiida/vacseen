from django.contrib import admin

from .models import User, Vaccine, Dose

admin.site.register(Vaccine)
admin.site.register(Dose)
