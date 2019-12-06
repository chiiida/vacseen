from django.contrib import admin
from .models import VaccineModel, DoseModel, Vaccine, Dose, Outbreak

admin.site.register(VaccineModel)
admin.site.register(DoseModel)
admin.site.register(Vaccine)
admin.site.register(Dose)
admin.site.register(Outbreak)
