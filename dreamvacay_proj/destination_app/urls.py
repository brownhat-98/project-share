from django.urls import path
from .views import *

urlpatterns = [
    path('', base, name='home'),
    path('view_dest/', view_destination_view, name='base'),

    path('register/', Register_user, name='register'),
    path('login/', loginUser, name='login'),
    path('logout/', logoutUser, name='logout'),
    path('edit_profile/', edit_profile, name='edit_profile'),
    path('user_profile/', user_details, name='user_profile'),
    
    path('api/dest/', add_destination.as_view(), name='api_add_dest'),
    path('api/dest/<int:pk>/', view_destination.as_view(), name='api_view_dest'),
    path('api/dest/<int:pk>/edit/', edit_destination.as_view(), name='api_edit_dest'),
    path('api/dest/<int:pk>/delete/', del_destination.as_view(), name='api_delete_dest'),
    path('api/dest/search/<str:name>/', search_destination.as_view(), name='api_search_dest'),

    path('detail_dest/<int:pk>/', detail_destination, name='detail_dest'),
    path('add_dest/', add_destination_view, name='add_dest'),
    path('view_dest/', view_destination_view, name='view_dest'),
    path('edit_dest/<int:pk>/', edit_destination_view, name='edit_dest'),
    path('delete_dest/<int:pk>/', delete_destination_view, name='delete_dest'),
    path('search_dest/', search_destination_view, name='search_dest'),
    
   
]
