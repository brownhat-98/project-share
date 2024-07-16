from django import forms
from .models import PatientProfile, TreatmentHistory, MedicalHistory, Billing
from doctor.models import Consultation

class TreatmentHistoryForm(forms.ModelForm):
    class Meta:
        model = TreatmentHistory
        fields = ['diagnosis', 'consultations']

class MedicalHistoryForm(forms.ModelForm):
    class Meta:
        model = MedicalHistory
        fields = '__all__'

class BillingForm(forms.ModelForm):
    class Meta:
        model = Billing
        fields = ['patient','doctor','description', 'medicines', 'amount','paid','total']
