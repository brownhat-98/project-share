from django import forms
from .models import DoctorProfile, Schedule, Prescription, Consultation, Medicines
from administration.models import Department

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = fields = ['doctor', 'date', 'start_time', 'end_time', 'department']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = '__all__'

class ConsultationForm(forms.ModelForm):
    class Meta:
        model = Consultation
        fields = '__all__'

class MedicinesForm(forms.ModelForm):
    class Meta:
        model = Medicines
        fields = '__all__'