from django.contrib import admin
from .models import VaccineModel, DoseModel, Vaccine, Dose

admin.site.register(VaccineModel)
admin.site.register(DoseModel)
admin.site.register(Vaccine)
admin.site.register(Dose)
