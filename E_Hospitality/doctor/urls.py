from django.urls import path
from . import views

urlpatterns = [
    path('doctorprofile/', views.doctorprofile, name='base'),

    path('schedule_list/', views.schedule_list, name='schedule_list'),
    path('view_schedule/<int:pk>', views.view_schedule, name='view_schedule'),
    path('view_schedule', views.view_schedule, name='view_schedule'),
    path('add_schedule', views.add_schedule, name='add_schedule'),
    path('edit_schedule/<int:pk>', views.edit_schedule, name='edit_schedule'),

    path('create_prescription/', views.create_prescription, name='create_prescription'),
    path('prescription_list/', views.prescription_list, name='prescription_list'),
    path('view_prescription/<int:pk>', views.view_prescription, name='view_prescription'),
    path('edit_prescription/<int:pk>', views.edit_prescription, name='edit_prescription'),

    path('add_consultation/', views.add_consultation, name='add_consultation'),
    path('view_consultation/', views.view_consultation, name='view_consultation'),
    path('view_consultation/<int:pk>', views.view_consultation, name='view_consultation'),
    path('edit_consultation/<int:pk>', views.edit_consultation, name='edit_consultation'),

    path('add_medicine/', views.add_medicine, name='add_medicine'),
    path('view_medicines/', views.view_medicines, name='view_medicines'),
    path('edit_medicine/<int:pk>', views.edit_medicine, name='edit_medicine'),
]