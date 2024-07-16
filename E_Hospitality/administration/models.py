from django.db import models
from django.contrib.auth.models import User

class AdminProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.IntegerField(null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    role = models.CharField(max_length=20, default='Admin')

    def __str__(self):
        return self.name

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone = models.IntegerField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=200)
    facilities = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    equipment = models.CharField(max_length=200, null=True, blank=True)
    doctor = models.ForeignKey('doctor.DoctorProfile', on_delete=models.CASCADE, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)

    def __str__(self):
        return self.name

class AppointmentSchedule(models.Model):
    doctor = models.ForeignKey('doctor.DoctorProfile', on_delete=models.CASCADE)
    patient = models.ForeignKey('patient.PatientProfile', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    description = models.TextField(null=True, blank=True)
    symptoms = models.TextField(null=True, blank=True)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    time_of_creation = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.doctor.user.username} - {self.department.name} - {self.date} {self.start_time}-{self.end_time}"
