from django.urls import path
from . import views

urlpatterns = [
    path('patientprofile', views.patientprofile, name='patientprofile'),

    path('add_treatment_history/', views.add_treatment_history, name='add_treatment_history'),
    path('edit_treatment_history/<int:pk>', views.edit_treatment_history, name='edit_treatment_history'),
    path('treatment_history_list/', views.treatment_history_list, name='treatment_history_list'),
    path('delete_treatment_history/<int:pk>', views.delete_treatment_history, name='delete_treatment_history'),

    path('medical_history_list/', views.medical_history_list, name='medical_history_list'),
    path('add_medical_history/', views.add_medical_history, name='add_medical_history'),
    path('edit_medical_history/<int:pk>', views.edit_medical_history, name='edit_medical_history'),
    path('delete_medical_history/<int:pk>', views.delete_medical_history, name='delete_medical_history'),

    path('list_invoices/', views.list_invoices, name='list_invoices'),
    path('billing/create/', views.create_invoice, name='create_invoice'),
    path('billing/edit/<int:pk>/', views.edit_invoice, name='edit_invoice'),
    path('billing/view/<int:pk>/', views.view_invoice, name='view_invoice'),
    path('billing/checkout/<int:pk>/', views.create_checkout_session, name='create_checkout_session'),
    path("success/", views.success, name='success'),
    path("cancel/", views.cancel, name='cancel'),
]