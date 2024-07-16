from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from .decorators import admin_required
from .models import Schedule
from .forms import *
from django.utils import timezone

from administration.models import Department, AppointmentSchedule
from patient.models import PatientProfile,TreatmentHistory

@login_required(login_url='login')
def doctorprofile(request):
    return render(request,'doctor/doctor.html')

#_______________________________________________________________SCHEDULE VIEWS↓
@login_required(login_url='login')
def schedule_list(request):
    schedules=Schedule.objects.all()
    return render(request,'doctor/schedule/schedule_list.html',{'schedules': schedules})

@login_required(login_url='login')
def view_schedule(request, pk):
    schedule=Schedule.objects.get(id=pk)
    return render(request,'doctor/schedule/view_schedule.html',{'schedule': schedule})

@login_required
@admin_required
def add_schedule(request):
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        if form.is_valid():
            schedule = form.save()
            form.save()
            return redirect('view_schedule', schedule.id)
        else:
            messages.error(request, 'Error adding schedule')
    else:
        form = ScheduleForm()
    return render(request,'doctor/schedule/add_schedule.html',{'form': form})

@login_required(login_url='login')
def edit_schedule(request, pk):
    schedule=Schedule.objects.get(id=pk)
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            schedule = form.save()
            form.save()
            return redirect('view_schedule', schedule.id)
        else:
            messages.error(request, 'Error adding schedule')
    else:
        form = ScheduleForm(instance=schedule)
    return render(request,'doctor/schedule/edit_schedule.html',{'form': form})    


#_______________________________________________________________SCHEDULE VIEWS↑
#_______________________________________________________________APPPOINTMENT VIEWS↓
@login_required(login_url='login')
def appointment_list(request):
    appointments = AppointmentSchedule.objects.filter(doctor=request.user)
    return render(request, 'doctor/appointment/appointment_list.html', {'appointments': appointments})

#_______________________________________________________________APPPOINTMENT VIEWS↑


@login_required(login_url='login')
def create_prescription(request):
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.save()
            form.save_m2m() 
            return redirect('view_prescription' , prescription.id)
    else:
        form = PrescriptionForm()
    return render(request, 'doctor/prescription/create_prescription.html', {'form': form})


@login_required(login_url='login')
def view_prescription(request, pk=None):
    if pk:
        prescription = get_object_or_404(Prescription, id=pk)
    else:
        if request.user.groups.filter(name='Patient').exists():
            prescription = get_object_or_404(Prescription, patient=request.user.patientprofile)
        else:
            prescription = get_object_or_404(Prescription, doctor=request.user.doctorprofile)

    return render(request, 'doctor/prescription/view_prescription.html', {'prescription': prescription})

@login_required(login_url='login')
def edit_prescription(request, pk):
    prescription=Prescription.objects.get(id=pk)
    if request.method == 'POST':
        form = PrescriptionForm(request.POST, instance=prescription)
        if form.is_valid():
            prescription = form.save()
            form.save()
            return redirect('view_prescription', prescription.id)
        else:
            messages.error(request, 'Error adding prescription')
    else:
        form = PrescriptionForm(instance=prescription)
    return render(request,'doctor/prescription/edit_prescription.html',{'form': form})


#_______________________________________________________________PRESCRIPTION VIEWS↑

#_______________________________________________________________Consultation views↓
@login_required(login_url='login')
def add_consultation(request):
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            consultation = form.save()
            # Automatically create a TreatmentHistory entry
            TreatmentHistory.objects.create(
                patient=consultation.patient,
                diagnosis=consultation.diagnosis,
                consultations=consultation,
                date_created=timezone.now()
            )
            messages.success(request, 'Consultation added successfully!')
            return redirect('view_consultation')
        else:
            messages.error(request, 'Error adding consultation')
    else:
        form = ConsultationForm()
    return render(request, 'doctor/consultation/add_consultation.html', {'form': form})


@login_required(login_url='login')
def view_consultation(request):
    consultations = Consultation.objects.all()
    return render(request,'doctor/consultation/view_consultation.html',{'consultations': consultations})

@login_required(login_url='login')
def edit_consultation(request, pk):
    consultation=Consultation.objects.get(id=pk)
    if request.method == 'POST':
        form = ConsultationForm(request.POST, instance=consultation)
        if form.is_valid():
            consultation = form.save()
            form.save()
            return redirect('view_consultation', consultation.id)
        else:
            messages.error(request, 'Error adding consultation')
    else:
        form = ConsultationForm(instance=consultation)
    return render(request,'doctor/consultation/edit_consultation.html',{'form': form})
#_______________________________________________________________Consultation views↑

@login_required(login_url='login')
def add_medicine(request):
    if request.method == 'POST':
        form = MedicinesForm(request.POST)
        if form.is_valid():
            medicine = form.save()
            form.save()
            return redirect('view_medicines')
        else:
            messages.error(request, 'Error adding medicine')
    else:
        form = MedicinesForm()
    return render(request,'doctor/medicine/add_medicine.html',{'form': form})

@login_required(login_url='login')
def view_medicines(request):
    medicines = Medicines.objects.all()
    return render(request,'doctor/medicine/view_medicines.html',{'medicines': medicines})      

@login_required(login_url='login')
def edit_medicine(request, pk):
    medicine=Medicines.objects.get(id=pk)
    if request.method == 'POST':
        form = MedicinesForm(request.POST, instance=medicine)
        if form.is_valid():
            medicine = form.save()
            form.save()
            return redirect('view_medicine', medicine.id)
        else:
            messages.error(request, 'Error adding medicine')
    else:
        form = MedicinesForm(instance=medicine)
    return render(request,'doctor/medicine/edit_medicine.html',{'form': form})
