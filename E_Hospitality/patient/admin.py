# patients/admin.py
from django.contrib import admin
from .models import *

admin.site.register(PatientProfile)
admin.site.register(MedicalHistory)
admin.site.register(TreatmentHistory)
admin.site.register(Billing)