# doctors/admin.py
from django.contrib import admin
from .models import *

admin.site.register(DoctorProfile)
admin.site.register(Schedule)
admin.site.register(Prescription)
admin.site.register(Consultation)