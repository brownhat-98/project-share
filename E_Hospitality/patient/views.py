from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import stripe
from django.conf import settings
from django.urls import reverse


from .forms import BillingForm as InvoiceForm
from .forms import *
from .models import *
from .models import Billing as Invoice

def patientprofile(request):
    return render(request, 'patient/patient.html')

@login_required(login_url='login')
def treatment_history_list(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    histories = TreatmentHistory.objects.filter(patient=patient)
    return render(request, 'patient/treatment_history/treatment_history_list.html', {'histories': histories})

@login_required(login_url='login')
def view_treatment_history(request, pk):
    history = get_object_or_404(TreatmentHistory, pk=pk)
    return render(request, 'patient/treatment_history/view_treatment_history.html', {'treatment_history': history})


@login_required
def add_treatment_history(request):
    if request.method == 'POST':
        form = TreatmentHistoryForm(request.POST)
        if form.is_valid():
            history = form.save(commit=False)
            history.patient = get_object_or_404(PatientProfile, user=request.user)
            history.save()
            messages.success(request, 'Treatment history added successfully.')
            return redirect('treatment_history_list')
    else:
        form = TreatmentHistoryForm()
    return render(request, 'patient/treatment_history/treatment_history_form.html', {'form': form})

@login_required
def edit_treatment_history(request, pk):
    history = get_object_or_404(TreatmentHistory, pk=pk)
    if request.method == 'POST':
        form = TreatmentHistoryForm(request.POST, instance=history)
        if form.is_valid():
            form.save()
            messages.success(request, 'Treatment history updated successfully.')
            return redirect('treatment_history_list')
    else:
        form = TreatmentHistoryForm(instance=history)
    return render(request, 'patient/treatment_history/treatment_history_form.html', {'form': form})

@login_required
def delete_treatment_history(request, pk):
    history = get_object_or_404(TreatmentHistory, pk=pk)
    if request.method == 'POST':
        history.delete()
        messages.success(request, 'Treatment history deleted successfully.')
        return redirect('treatment_history_list')
    return render(request, 'patient/treatment_history/treatment_history_confirm_delete.html', {'history': history})

# Medical History Views
@login_required(login_url='login')
def medical_history_list(request):
    patient = get_object_or_404(PatientProfile, user=request.user)
    histories = MedicalHistory.objects.filter(patient=patient)
    return render(request, 'patient/medical_history/medical_history_list.html', {'histories': histories})

@login_required(login_url='login')
def view_medical_history(request, pk):
    history = get_object_or_404(MedicalHistory, pk=pk)
    return render(request, 'patient/medical_history/view_medical_history.html', {'medical_history': history})

@login_required(login_url='login')
def add_medical_history(request):
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            history = form.save(commit=False)
            history.patient = get_object_or_404(PatientProfile, user=request.user)
            history.save()
            messages.success(request, 'Medical history added successfully.')
            return redirect('medical_history_list')
    else:
        form = MedicalHistoryForm()
    return render(request, 'patient/medical_history/medical_history_form.html', {'form': form})

@login_required
def edit_medical_history(request, pk):
    history = get_object_or_404(MedicalHistory, pk=pk)
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST, instance=history)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medical history updated successfully.')
            return redirect('medical_history_list')
    else:
        form = MedicalHistoryForm(instance=history)
    return render(request, 'patient/medical_history/medical_history_form.html', {'form': form})

@login_required
def delete_medical_history(request, pk):
    history = get_object_or_404(MedicalHistory, pk=pk)
    if request.method == 'POST':
        history.delete()
        messages.success(request, 'Medical history deleted successfully.')
        return redirect('medical_history_list')
    return render(request, 'patient/medical_history/medical_history_confirm_delete.html', {'history': history})


#___________________________________________________BILLING VIEWS↓
@login_required
def list_invoices(request):
    if request.user.groups.filter(name='Admin').exists():
        invoices = Billing.objects.all()
    else:
        patient_profile = get_object_or_404(PatientProfile, user=request.user)
        invoices = Billing.objects.filter(patient=patient_profile)
    return render(request, 'patient/billing/invoice_list.html', {'invoices': invoices})

@login_required
def create_invoice(request):
    if request.method == 'POST':
        form = BillingForm(request.POST)
        if form.is_valid():
            billing = form.save(commit=False)
            billing.save()
            messages.success(request, 'Invoice created successfully.')
            return redirect('view_invoice', pk=billing.pk)
    else:
        form = BillingForm()
    return render(request, 'patient/billing/invoice_form.html', {'form': form})


@login_required
def edit_invoice(request, pk):
    billing = get_object_or_404(Billing, pk=pk)
    if request.method == 'POST':
        form = BillingForm(request.POST, instance=billing)
        if form.is_valid():
            form.save()
            messages.success(request, 'Invoice updated successfully.')
            return redirect('view_invoice', pk=billing.pk)
    else:
        form = BillingForm(instance=billing)
    return render(request, 'patient/billing/invoice_form.html', {'form': form})


@login_required
def view_invoice(request, pk):
    billing = get_object_or_404(Billing, pk=pk)
    return render(request, 'patient/billing/invoice_detail.html', {'billing': billing})



#____________________________________________________________PAYMENTGATEWAY
@login_required
def create_checkout_session(request, pk):
    billing = get_object_or_404(Billing, pk=pk)

    if request.method == 'POST':
        stripe.api_key = settings.STRIPE_SECRET_KEY

        line_item = {
            'price_data': {
                'currency': 'INR',
                'unit_amount': int(billing.amount) * 100,
                'product_data': {
                    'name': billing.description,
                },
            },
            'quantity': 1,
        }

        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[line_item],
            mode='payment',
            success_url=request.build_absolute_uri(reverse('success', args=[billing.pk])),
            cancel_url=request.build_absolute_uri(reverse('cancel')),
        )
        return redirect(checkout_session.url, code=303)

    return render(request, 'billing/view_invoice.html', {'billing': billing})

# #____________________________________________________________PAYMENTSUCCESS
@login_required
def success(request,pk):
    billing = get_object_or_404(Billing, pk=pk)
    billing.paid = True
    billing.save()
    return render(request, 'patient/billing/success.html')



# #____________________________________________________________PAYMENTFAIL
@login_required
def cancel(request):
    return render(request, 'patient/billing/cancel.html')