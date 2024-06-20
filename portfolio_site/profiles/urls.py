from django.urls import path
from .views import *

urlpatterns = [
    path('projects/', project_view, name='project_view'),

    path('profile/', profile_view, name='profile_view'),
    path('edit-profile/', edit_profile, name='edit_profile'),
     
    path('portfolio/<int:id>/', portfolio_view, name='portfolio_view'),
    path('portfolio/', portfolio_view, name='portfolio_view'),
    path('portfolio/edit/', edit_portfolio_view, name='edit_portfolio'),
    path('add-custom-field/', add_custom_field, name='add_custom_field'),
    path('delete-custom-field/<int:field_id>/', delete_custom_field, name='delete_custom_field'),

    path('certificates/<int:id>/', certificate_detail, name='certificate_detail'),
    path('certificates/add/', certificate_add, name='certificate_add'),
    path('certificates/edit/<int:id>/', certificate_edit, name='certificate_edit'),
    path('certificates/delete/<int:id>/', certificate_delete, name='certificate_delete'),
    
    path('projects/add/', add_project, name='add_project'),
    path('projects/edit/<int:project_id>/', edit_project, name='edit_project'),
    path('projects/delete/<int:project_id>/', delete_project, name='delete_project'),
    path('projects/<int:id>/', project_detail_view, name='project_detail'),
    path('projects/<int:id>/edit_image/<int:image_id>/', edit_project_image_view, name='edit_project_image'),
    path('projects/<int:id>/delete_image/<int:image_id>/', delete_project_image_view, name='delete_project_image'),

    path('search/', search, name='search'),
    path('register/', Register_user, name='register'),
    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('dash/', dash_view, name='dash'),  
    path('', base_view, name='base'),

]    