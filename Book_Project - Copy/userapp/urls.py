from django.urls import path
from . import views

urlpatterns = [
    path("",views.user_products,name='userproducts'),
    path('editprofile/', views.edit_profile , name='edit_profile'),

    path("dash/",views.userdash,name='userdash'),
    path("products/",views.user_products,name='userproducts'),
    path("details/",views.user_details,name='userdetails'),
    path("orders/<int:pk>",views.user_orders,name='userorders'),
    path("createorder/<int:pk>",views.create_order,name='createorder'),
    path("updateorder/<int:pk>",views.update_order,name='updateorder'),
    path("deleteorder/<int:pk>",views.delete_order,name='deleteorder'),

    path("cartadd/", views.cart_add, name='cart_add'),
    path("cartsum/", views.cart_sum, name='cart_sum'),
    path("cart/update/", views.cart_update, name='cart_update'),
    path("cart/delete/", views.cart_delete, name='cart_delete'),
    path('cart/place_order/', views.place_order, name='place_order'),
    path("create-checkout-session/", views.create_checkout_session, name='create-checkout-session'),
    path("success/", views.success, name='success'),
    path("cancel/", views.cancel, name='cancel'),

]