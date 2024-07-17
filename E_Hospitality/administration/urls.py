from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView, PasswordChangeView
from django.views.generic import TemplateView

from . import views
from .views import *


urlpatterns = [
    path('', views.base_view, name='base_view'),

    path('login/',views.login_user , name='login'),
    path('logout/',views.logout_user , name='logout'),
    path('change_password/',PasswordChangeView.as_view(template_name='administration/user/change_password.html'), name='password_change'),

    path('profile/view/', views.profile_view, name='profile_view'),
    path('profile/edit/<int:user_id>/', views.profile_edit, name='profile_edit'),
    path('profile/view/<int:user_id>/', views.profile_view, name='profile_view'),
    path('profile/confirm_convert/<int:user_id>/', views.convert_roles_confirm, name='confirm_convert'),
    path('convert_user/<int:user_id>/<str:new_group>/', views.convert_user, name='convert_user'),
    path('user_list/', views.user_list, name='user_list'),

    path('view_hospital/',views.view_hospital, name='view_hospital'),
    path('add_hospital/',views.add_hospital, name='add_hospital'),
    path('edit_hospital/',views.edit_hospital, name='edit_hospital'),

    path('add_department/',views.add_department, name='add_department'),
    path('edit_department/<int:department_id>/',views.edit_department, name='edit_department'),
    path('view_department/<int:department_id>/',views.view_department, name='view_department'),
    path('department_list/',views.department_list, name='department_list'),

    path('appointment/create/', create_appointment, name='create_appointment'),
    path('appointment/view/<int:pk>/', views.view_appointment, name='view_appointment'),
    path('appointment/list/', views.appointment_list, name='appointment_list'),
    path('appointment/success/', TemplateView.as_view(template_name='administration/appointment/appointment_success.html'), name='appointment_success'),

]
