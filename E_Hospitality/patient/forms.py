from django import forms
from .models import PatientProfile, TreatmentHistory, MedicalHistory, Billing
from doctor.models import Consultation

class TreatmentHistoryForm(forms.ModelForm):
    class Meta:
        model = TreatmentHistory
        fields = '__all__'

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = '__all__'

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = '__all__'
