from django.db import models
from django.contrib.auth.models import User
from administration.models import Department, AppointmentSchedule

class DoctorProfile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    phone = models.CharField(max_length=200, null=True, blank=True)
    profile_pic = models.ImageField(null=True, blank=True)
    specialization = models.CharField(max_length=200, null=True, blank=True)
    license_no = models.CharField(max_length=200, null=True, blank=True)
    qualification = models.CharField(max_length=200, null=True, blank=True)
    experience = models.CharField(max_length=200, null=True, blank=True)
    assigned_dept = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)
    appointment = models.ForeignKey(AppointmentSchedule, on_delete=models.CASCADE, max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    role = models.CharField(max_length=20, default='Doctor')
    
    STATUS_CHOICES = (
        ('House on Call', 'House on Call'),
        ('On call', 'On call'),
        ('Intern', 'Intern'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='House on Call')

    def __str__(self):
        return f'{self.name} - {self.specialization}'

class Schedule(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    date = models.DateField()
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.doctor.user.username} - {self.date} - {self.time}'

class Medicines(models.Model):
    name=models.CharField(max_length=200)
    brand=models.CharField(max_length=200)
    price=models.CharField(max_length=200)
    description=models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Prescription(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey('patient.PatientProfile', on_delete=models.CASCADE)
    prescription = models.TextField()
    medicines = models.ManyToManyField(Medicines)
    consumption_instruction = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Prescription for {self.patient}'

class Consultation(models.Model):
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    patient = models.ForeignKey('patient.PatientProfile', on_delete=models.CASCADE)
    diagnosis = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    prescription = models.ForeignKey(Prescription, on_delete=models.CASCADE)

    def __str__(self):
        return f'Consultation with {self.patient}'

