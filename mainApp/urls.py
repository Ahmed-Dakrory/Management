

from django.urls import path
from . import views

app_name='mainApp'
urlpatterns = [
    path('',views.home,name='home'),
    path('show_companies/',views.show_companies,name='show_companies'),
    path('show_representatives/',views.show_representatives,name='show_representatives'),
    path('show_items/',views.show_items,name='show_items'),





    path('checkUniquenessOfserial_start/',views.checkUniquenessOfserial_start,name='checkUniquenessOfserial_start'),
    

    # category
    path('listOf_category/',views.listOf_category,name='listOf_category'),
    path('getListOf_category/',views.getListOf_category,name='getListOf_category'),
    path('addnew_category/',views.addnew_category,name='addnew_category'),
    path('delete_category/',views.delete_category,name='delete_category'),



    # factory
    path('listOf_factory/',views.listOf_factory,name='listOf_factory'),
    path('getListOf_factory/',views.getListOf_factory,name='getListOf_factory'),
    path('addnew_factory/',views.addnew_factory,name='addnew_factory'),
    path('delete_factory/',views.delete_factory,name='delete_factory'),


    
    # sector
    path('listOf_sector/',views.listOf_sector,name='listOf_sector'),
    path('getListOf_sector/',views.getListOf_sector,name='getListOf_sector'),
    path('addnew_sector/',views.addnew_sector,name='addnew_sector'),
    path('delete_sector/',views.delete_sector,name='delete_sector'),


    
    # company
    path('listOf_company/',views.listOf_company,name='listOf_company'),
    path('getListOf_company/',views.getListOf_company,name='getListOf_company'),
    path('addnew_company/',views.addnew_company,name='addnew_company'),
    path('delete_company/',views.delete_company,name='delete_company'),

]