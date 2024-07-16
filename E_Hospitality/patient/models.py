from django.db import models
from django.contrib.auth.models import User

class PatientProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    role = models.CharField(max_length=20, default='Patient')

    def __str__(self):
        return self.name

class TreatmentHistory(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    consultations = models.ForeignKey('doctor.Consultation', on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.diagnosis

class MedicalHistory(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    description = models.TextField()
    age = models.CharField(max_length=10)
    gender = models.CharField(max_length=10)
    blood_group = models.CharField(max_length=10)
    height = models.CharField(max_length=10)
    weight = models.CharField(max_length=10)
    allergies = models.TextField()
    treatment_history = models.ForeignKey(TreatmentHistory, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

class Billing(models.Model):
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    description = models.TextField()
    doctor = models.ForeignKey('doctor.DoctorProfile', on_delete=models.CASCADE)
    medicines = models.ForeignKey('doctor.Medicines', on_delete=models.CASCADE, null=True, blank=True)
    amount = models.CharField(max_length=10, null=True, blank=True)
    paid = models.BooleanField(default=False)
    total = models.CharField(max_length=10, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
