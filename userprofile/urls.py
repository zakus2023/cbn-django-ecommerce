from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    
    path('myaccount/', views.myaccount, name='myaccount'),
    path('login/', auth_views.LoginView.as_view(template_name='userprofile/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
    path('mystore/', views.mystore, name='mystore'),
    path('mystore/add_product/', views.add_product, name='add_product'),
    path('mystore/update_product/<int:id>/', views.update_product, name='update_product'),
    path('mystore/delete_product/<int:id>/', views.delete_product, name='delete_product'),
    path('vendor/<int:id>/', views.vendor_detail, name='vendor_detail')
]