from django.urls import path
from . import views

urlpatterns = [
    path('patientprofile', views.patientprofile, name='patientprofile'),

    path('add_treatment_history/', views.add_treatment_history, name='add_treatment_history'),
    path('edit_treatment_history/<int:pk>', views.edit_treatment_history, name='edit_treatment_history'),
    path('view_treatment_history/<int:pk>', views.view_treatment_history, name='view_treatment_history'),
    path('view_treatment_history/', views.view_treatment_history, name='view_treatment_history'),

    path('add_medical_history/', views.add_medical_history, name='add_medical_history'),
    path('edit_medical_history/<int:pk>', views.edit_medical_history, name='edit_medical_history'),
    path('view_medical_history/<int:pk>', views.view_medical_history, name='view_medical_history'),
    path('view_medical_history/', views.view_medical_history, name='view_medical_history'),

    path('add_invoice/', views.add_invoice, name='add_invoice'),
    path('edit_invoice/<int:pk>', views.edit_invoice, name='edit_invoice'),
    path('view_invoice/<int:pk>', views.view_invoice, name='view_invoice'),
]