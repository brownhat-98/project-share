from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import BillingForm as InvoiceForm
from .forms import *
from .models import *
from .models import Billing as Invoice

def patientprofile(request):
    return render(request, 'patient/patient.html')

#___________________________________________________TREATMENT HISTORY VIEWS↓
@login_required(login_url='login')
def add_treatment_history(request):
    if request.method == 'POST':
        form = TreatmentHistoryForm(request.POST)
        if form.is_valid():
            treatment_history = form.save()
            return redirect('view_treatment_history', treatment_history.id)
        else:
            messages.error(request, 'Error adding treatment history')
    else:
        form = TreatmentHistoryForm()
    return render(request, 'patient/treatment_history/add_treatment_history.html', {'form': form})

@login_required(login_url='login')
def edit_treatment_history(request, pk):
    treatment_history = TreatmentHistory.objects.get(id=pk)
    if request.method == 'POST':
        form = TreatmentHistoryForm(request.POST, instance=treatment_history)
        if form.is_valid():
            treatment_history = form.save()
            return redirect('view_treatment_history', treatment_history.id)
        else:
            messages.error(request, 'Error editing treatment history')
    else:
        form = TreatmentHistoryForm(instance=treatment_history)
    return render(request, 'patient/treatment_history/edit_treatment_history.html', {'form': form})

@login_required(login_url='login')
def view_treatment_history(request, pk):
    treatment_history = TreatmentHistory.objects.get(id=pk)
    return render(request, 'patient/treatment_history/view_treatment_history.html', {'treatment_history': treatment_history})


# @login_required(login_url='login')
# def view_treatment_history(request, pk=None):
#     treatment_history = None
#     if pk:
#         try:
#             treatment_history = TreatmentHistory.objects.get(id=pk)
#         except TreatmentHistory.DoesNotExist:
#             messages.error(request, 'Treatment history not found.')
#             return redirect('base_view')
#     else:
#         if request.user.groups.filter(name='Patient').exists():
#             treatment_history = TreatmentHistory.objects.filter(patient=request.user.patientprofile)
#         elif request.user.groups.filter(name='Doctor').exists():
#             treatment_history = TreatmentHistory.objects.filter(doctor=request.user.doctorprofile)
#         else:
#             messages.error(request, 'No treatment history found for this user.')
#             return redirect('base_view') 

#     return render(request, 'patient/treatment_history/view_treatment_history.html', {'treatment_history': treatment_history})

#___________________________________________________MEDICAL HISTORY VIEWS↓
@login_required(login_url='login')
def add_medical_history(request):
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST)
        if form.is_valid():
            medical_history = form.save()
            return redirect('view_medical_history', medical_history.id)
        else:
            messages.error(request, 'Error adding medical history')
    else:
        form = MedicalHistoryForm()
    return render(request, 'patient/medical_history/add_medical_history.html', {'form': form})

@login_required(login_url='login')
def edit_medical_history(request, pk):
    medical_history = MedicalHistory.objects.get(id=pk)
    if request.method == 'POST':
        form = MedicalHistoryForm(request.POST, instance=medical_history)
        if form.is_valid():
            medical_history = form.save()
            return redirect('view_medical_history', medical_history.id)
        else:
            messages.error(request, 'Error editing medical history')
    else:
        form = MedicalHistoryForm(instance=medical_history)
    return render(request, 'patient/medical_history/edit_medical_history.html', {'form': form})

@login_required(login_url='login')
def view_medical_history(request, pk=None):
    medical_history = None
    if pk:
        try:
            medical_history = MedicalHistory.objects.get(id=pk)
        except MedicalHistory.DoesNotExist:
            messages.error(request, 'Medical history not found.')
            return redirect('base_view')
    else:
        if request.user.groups.filter(name='Patient').exists():
            medical_history = MedicalHistory.objects.filter(patient=request.user.patientprofile)
        elif request.user.groups.filter(name='Doctor').exists():
            medical_history = MedicalHistory.objects.filter(doctor=request.user.doctorprofile)
        else:
            messages.error(request, 'No medical history found for this user.')
            return redirect('base_view')

    return render(request, 'patient/medical_history/view_medical_history.html', {'medical_history': medical_history})

#___________________________________________________BILLING VIEWS↓
@login_required(login_url='login')
def add_invoice(request):
    if request.method == 'POST':
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save()
            return redirect('view_invoice', invoice.id)
        else:
            messages.error(request, 'Error adding invoice')
    else:
        form = InvoiceForm()
    return render(request, 'patient/Billing/add_invoice.html', {'form': form})

@login_required(login_url='login')
def edit_invoice(request, pk):
    invoice = Invoice.objects.get(id=pk)
    if request.method == 'POST':
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            invoice = form.save()
            return redirect('view_invoice', invoice.id)
        else:
            messages.error(request, 'Error editing invoice')
    else:
        form = InvoiceForm(instance=invoice)
    return render(request, 'patient/Billing/edit_invoice.html', {'form': form})

@login_required(login_url='login')
def view_invoice(request, pk=None):
    invoice = None
    if pk:
        try:
            invoice = Invoice.objects.get(id=pk)
        except Invoice.DoesNotExist:
            messages.error(request, 'Invoice not found.')
            return redirect('base_view')  # Replace 'base_view' with an appropriate view
    else:
        if request.user.groups.filter(name='Patient').exists():
            invoice = Invoice.objects.filter(patient=request.user.patientprofile)
        elif request.user.groups.filter(name='Doctor').exists():
            invoice = Invoice.objects.filter(doctor=request.user.doctorprofile)
        else:
            messages.error(request, 'No invoice found for this user.')
            return redirect('base_view')  # Replace 'base_view' with an appropriate view

    return render(request, 'patient/Billing/view_invoice.html', {'invoice': invoice})



# #____________________________________________________________PAYMENTGATEWAY
# def create_checkout_session(request):
#     cart = Cart(request)

#     if request.method == 'POST':
#         line_items=[]
#         stripe.api_key=settings.STRIPE_SECRET_KEY

#         for item in cart.get_products():

#             if item:
#                 line_item={
#                     'price_data':{
#                         'currency':'INR',
#                         'unit_amount':int(item.price *100),
#                         'product_data':{
#                             'name':item.title
#                         },
#                     },
#                     'quantity':cart.get_quantity(item.id)
#                 }
#                 line_items.append(line_item)


#         if line_items:
#             checkout_session=stripe.checkout.Session.create(
#                 payment_method_types=['card'],
#                 line_items=line_items,
#                 mode='payment',
#                 success_url=request.build_absolute_uri(reverse('success')),
#                 cancel_url=request.build_absolute_uri(reverse('cancel'))
#             )
#             return redirect(checkout_session.url,code=303)

# #____________________________________________________________PAYMENTSUCCESS
# def success(request):
#     cart = Cart(request)
#     cart_items=cart.get_products()

#     for item in cart_items:
#         product=item
#         if product.quantity>=cart.get_quantity(item.id):
#             product.quantity-=cart.get_quantity(item.id)
#             product.save()

#     # cart_items.delete()
#     cart.clear()

#     return render(request,'userapp/success.html')



# #____________________________________________________________PAYMENTFAIL
# def cancel(request):
#     return render(request,'userapp/cancel.html')

