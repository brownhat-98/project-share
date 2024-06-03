from django.urls import path
from . import views

urlpatterns = [

    path("",views.base,name='home'),
    path("createview",views.createBook,name='create'),
    path("author/",views.CreateAuthor,name='author'),
    path("listview/",views.listbook,name='listview'),
    path("regusers/",views.Registered_users,name='regusers'),
    path("detailsview/<int:book_id>/",views.detailsView,name='details'),
    path("updateview/<int:book_id>/",views.updateBook,name='update'),
    path("deleteview/<int:book_id>/",views.deleteView,name='delete'),
    path('deleteAuthorView/<int:book_id>/',views.DeleteAuthor,name='deleteAuthorView'),
    path('updateAuthor/<int:book_id>/',views.UpdateAuthor,name="updateAuthor"),
    path('search/',views.Search_Book,name='search'),
    
    path('admindash',views.admindash,name='admindash'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.Register_user, name='register'),
    path('login/', views.loginUser, name='login'),



]
