

from django.urls import path
from . import views

app_name='userApp'
urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('logout/',views.user_logout,name='logout'),

    
    path('listOf_user/',views.listOf_user,name='listOf_user'),
    path('getListOf_user/',views.getListOf_user,name='getListOf_user'),
    path('addnew_user/',views.addnew_user,name='addnew_user'),
    path('delete_user/',views.delete_user,name='delete_user'),


    
    path('listOf_role/',views.listOf_role,name='listOf_role'),
    path('getListOf_role/',views.getListOf_role,name='getListOf_role'),
    path('addnew_role/',views.addnew_role,name='addnew_role'),


    
]