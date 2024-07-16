# admin/admin.py
from django.contrib import admin
from .models import AdminProfile,Hospital, Department, AppointmentSchedule


admin.site.register(AdminProfile)
admin.site.register(Hospital)
admin.site.register(Department)
admin.site.register(AppointmentSchedule)
