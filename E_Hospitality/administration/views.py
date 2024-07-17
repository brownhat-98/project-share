from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta, datetime

from doctor.models import DoctorProfile, Schedule
from patient.models import PatientProfile
from .models import AdminProfile, Hospital, Department, AppointmentSchedule
from .forms import CreateUserForm, AdminProfileForm, DoctorProfileForm, PatientProfileForm, HospitalForm, DepartmentForm, AppointmentScheduleForm
from .decorators import admin_required


@login_required(login_url='login')
def base_view(request):
    return render(request, 'base.html')

#____________________________________________________________________AUTH VIEWS↓
def register_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Automatically assign user to 'Patient' group
            patient_group = Group.objects.get(name='Patient')
            user.groups.add(patient_group)

            # Create a default PatientProfile
            PatientProfile.objects.create(user=user, name=user.username, email=user.email)

            return redirect('login')
    else:
        form = CreateUserForm()
    return render(request, 'administration/user/register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('base_view')
            else:
                messages.error(request, "The username or password is wrong")
    else:
        form = AuthenticationForm()
    return render(request, 'administration/user/login.html', {'form': form})


@login_required(login_url='login')
def logout_user(request):
    if request.method == 'POST' or request.method == 'GET':
        logout(request)
    return render(request, 'administration/user/logout.html')
#____________________________________________________________________AUTH VIEWS↑

#____________________________________________________________________PROFILE VIEWS↓
@login_required(login_url='login')
def profile_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # Determine which profile form to use based on user's group
    if user.groups.filter(name='Admin').exists():
        profile_instance = get_object_or_404(AdminProfile, user=user)
        form_class = AdminProfileForm
    elif user.groups.filter(name='Doctor').exists():
        profile_instance = get_object_or_404(DoctorProfile, user=user)
        form_class = DoctorProfileForm
    else:  # Default to Patient profile for others
        profile_instance = get_object_or_404(PatientProfile, user=user)
        form_class = PatientProfileForm

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES, instance=profile_instance)
        if form.is_valid():
            form.save()
            return redirect('profile_view', user_id=user_id)
    else:
        form = form_class(instance=profile_instance)

    return render(request, 'administration/user/profile_edit.html', {'form': form, 'profile': profile_instance})


@login_required(login_url='login')
def profile_view(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    user_groups = list(user.groups.values_list('name', flat=True))

    if 'Admin' in user_groups:
        profile = get_object_or_404(AdminProfile, user=user)
    elif 'Doctor' in user_groups:
        profile = get_object_or_404(DoctorProfile, user=user)
    elif 'Patient' in user_groups:
        profile = get_object_or_404(PatientProfile, user=user)
    else:
        profile = None

    return render(request, 'administration/user/profile_view.html', {
        'profile': profile,
        'user_groups': user_groups
    })

#______________________________________________________________________PROFILE VIEWS↑

#______________________________________________________________________ROLE MANAGEMENT↓
@login_required(login_url='login')
@admin_required
def user_list(request):
    users = User.objects.all()
    user_data = []

    for user in users:
        profile = None
        if hasattr(user, 'adminprofile'):
            profile = user.adminprofile
        elif hasattr(user, 'doctorprofile'):
            profile = user.doctorprofile
        elif hasattr(user, 'patientprofile'):
            profile = user.patientprofile

        if profile:
            user_data.append({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': profile.role,
                'profile': profile,
            })

    return render(request, 'administration/user/user_list.html', {'users': user_data})


@login_required(login_url='login')
@admin_required
def convert_roles_confirm(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    # Determine which profile form to use based on user's group
    if user.groups.filter(name='Admin').exists():
        profile_instance = get_object_or_404(AdminProfile, user=user)
    elif user.groups.filter(name='Doctor').exists():
        profile_instance = get_object_or_404(DoctorProfile, user=user)
    else:  # Default to Patient profile for others
        profile_instance = get_object_or_404(PatientProfile, user=user)

    return render(request, 'administration/user/convert_roles_confirm.html', {'profile': profile_instance})


@login_required(login_url='login')
@admin_required
def convert_user(request, user_id, new_group):
    user = get_object_or_404(User, pk=user_id)
    current_group = user.groups.first().name if user.groups.exists() else None

    # Remove from current group and delete current profile
    if current_group == 'Admin':
        user.groups.remove(Group.objects.get(name='Admin'))
        AdminProfile.objects.filter(user=user).delete()
    elif current_group == 'Doctor':
        user.groups.remove(Group.objects.get(name='Doctor'))
        DoctorProfile.objects.filter(user=user).delete()
    elif current_group == 'Patient':
        user.groups.remove(Group.objects.get(name='Patient'))
        PatientProfile.objects.filter(user=user).delete()

    # Add to new group and create new profile
    new_group_instance = Group.objects.get(name=new_group)
    user.groups.add(new_group_instance)

    if new_group == 'Admin':
        AdminProfile.objects.create(user=user, name=f'{user.first_name} {user.last_name}', email=user.email, role=new_group)
    elif new_group == 'Doctor':
        DoctorProfile.objects.create(user=user, name=f'{user.first_name} {user.last_name}', email=user.email, role=new_group)
    elif new_group == 'Patient':
        PatientProfile.objects.create(user=user, name=f'{user.first_name} {user.last_name}', email=user.email, role=new_group)

    return redirect('profile_view', user_id=user_id)

#______________________________________________________________________ROLE MANAGEMENT↑

#______________________________________________________________________HOSPITAL CRUD↓
@login_required(login_url='login')
def view_hospital(request):
    hospital = get_object_or_404(Hospital, pk=1)
    return render(request, 'administration/hospital/view_hospital.html', {'hospital': hospital})


@login_required(login_url='login')
@admin_required
def add_hospital(request):
    form = HospitalForm()
    if request.method == 'POST':
        form = HospitalForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_hospital')

    return render(request, 'administration/hospital/add_hospital.html', {'form': form})


@login_required(login_url='login')
@admin_required
def edit_hospital(request):
    hospital = get_object_or_404(Hospital, pk=1)
    form = HospitalForm(instance=hospital)
    if request.method == 'POST':
        form = HospitalForm(request.POST, instance=hospital)
        if form.is_valid():
            form.save()
            return redirect('view_hospital')
        else:
            messages.error(request, 'Error updating hospital')
    else:
        form = HospitalForm(instance=hospital)

    return render(request, 'administration/hospital/edit_hospital.html', {'form': form})

#______________________________________________________________________HOSPITAL CRUD↑

#______________________________________________________________________Department CRUD↓
@login_required(login_url='login')
@admin_required
def add_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            department = form.save()
            department_id = department.id
            messages.success(request, 'Department added successfully')
            return redirect('view_department', department_id=department_id)
        else:
            messages.error(request, 'Error adding department')
    else:
        form = DepartmentForm()

    return render(request, 'administration/department/add_department.html', {'form': form})


@login_required(login_url='login')
@admin_required
def edit_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    form = DepartmentForm(instance=department)
    if request.method == 'POST':
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('view_department', department_id=department_id)
        else:
            messages.error(request, 'Error updating department')
    else:
        form = DepartmentForm(instance=department)

    return render(request, 'administration/department/edit_department.html', {'form': form})


@login_required(login_url='login')
def view_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    doctor = Department.objects.get(id=department_id).doctor
    return render(request, 'administration/department/view_department.html', {
        'department': department,
        'doctor': doctor,
    })


@login_required(login_url='login')
@admin_required
def delete_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    if request.method == 'POST':
        department.delete()
        return redirect('base_view')

    return render(request, 'administration/department/delete_department_confirm.html', {'department': department})

@login_required(login_url='login')
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'administration/department/department_list.html', {'departments': departments})

#______________________________________________________________________Department CRUD↑

#______________________________________________________________________APPOINTMENT CRUD↓
@login_required(login_url='login')
def appointment_list(request):
    if request.user.groups.filter(name='Doctor').exists():
        doctor = get_object_or_404(DoctorProfile, user=request.user)
        appointments = AppointmentSchedule.objects.filter(doctor=doctor)
    elif request.user.groups.filter(name='Patient').exists():
        patient = get_object_or_404(PatientProfile, user=request.user)
        appointments = AppointmentSchedule.objects.filter(patient=patient)
    else:
        appointments = AppointmentSchedule.objects.all()
    return render(request, 'administration/appointment/appointment_list.html', {'appointments': appointments})



@login_required(login_url='login')
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentScheduleForm(request.POST)
        if form.is_valid():
            patient = form.cleaned_data['patient']
            doctor = form.cleaned_data['doctor']
            date = form.cleaned_data['date']
            start_time = form.cleaned_data['start_time']
            end_time = (datetime.combine(date, start_time) + timedelta(minutes=30)).time()

            overlapping_appointments = AppointmentSchedule.objects.filter(
                doctor=doctor,
                date=date,
                start_time__lt=end_time,
                end_time__gt=start_time
            )

            if overlapping_appointments.exists():
                messages.error(request, 'The doctor is not available at the selected time.')
            else:
                appointment = AppointmentSchedule.objects.create(
                    patient=patient,
                    doctor=doctor,
                    department=form.cleaned_data['department'],
                    description=form.cleaned_data['description'],
                    symptoms=form.cleaned_data['symptoms'],
                    date=date,
                    start_time=start_time,
                    end_time=end_time
                )
                return redirect('appointment_success')  # Redirect to view with appointment ID
        else:
            messages.error(request, 'Please correct the errors below.')

    else:
        form = AppointmentScheduleForm()

    return render(request, 'administration/appointment/create_appointment.html', {
        'form': form,
        'patients': PatientProfile.objects.all(),
        'doctors': DoctorProfile.objects.all(),
        'departments': Department.objects.all(),
    })


@login_required(login_url='login')
def view_appointment(request,pk):
    appointment=get_object_or_404(AppointmentSchedule, pk=pk)
    return render(request, 'administration/appointment/view_appointment.html', {'appointment': appointment})

#______________________________________________________________________APPOINTMENT CRUD↑
