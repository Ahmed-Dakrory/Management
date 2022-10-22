

from django.urls import path
from . import views

app_name='mainApp'
urlpatterns = [
    path('',views.home,name='home'),
    path('show_companies/',views.show_companies,name='show_companies'),
    path('show_items/',views.show_items,name='show_items'),





    path('checkUniquenessOfserial_start/',views.checkUniquenessOfserial_start,name='checkUniquenessOfserial_start'),
    path('checkUniquenessOfpart_num/',views.checkUniquenessOfpart_num,name='checkUniquenessOfpart_num'),
    

    # category
    path('listOf_category/',views.listOf_category,name='listOf_category'),
    path('get_all_categories_by_name/',views.get_all_categories_by_name,name='get_all_categories_by_name'),
    path('getListOf_category/',views.getListOf_category,name='getListOf_category'),
    path('addnew_category/',views.addnew_category,name='addnew_category'),
    path('delete_category/',views.delete_category,name='delete_category'),



    # item
    path('item_by_part_num/',views.item_by_part_num,name='item_by_part_num'),
    path('listOf_item/',views.listOf_item,name='listOf_item'),
    path('getListOf_item/',views.getListOf_item,name='getListOf_item'),
    path('addnew_item/',views.addnew_item,name='addnew_item'),
    path('show_item/',views.show_item,name='show_item'),
    path('delete_item/',views.delete_item,name='delete_item'),




    path('out_stock_item/',views.out_stock_item,name='out_stock_item'),
    path('return_stock_item/',views.return_stock_item,name='return_stock_item'),

    # path('gen_listOf_item/',views.gen_listOf_item,name='gen_listOf_item'),
    


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




    # tranche
    path('listOf_tranche/',views.listOf_tranche,name='listOf_tranche'),
    path('getListOf_tranche/',views.getListOf_tranche,name='getListOf_tranche'),
    path('addnew_tranche/',views.addnew_tranche,name='addnew_tranche'),
    path('delete_tranche/',views.delete_tranche,name='delete_tranche'),


    
    # company
    path('listOf_company/',views.listOf_company,name='listOf_company'),
    path('getListOf_company/',views.getListOf_company,name='getListOf_company'),
    path('addnew_company/',views.addnew_company,name='addnew_company'),
    path('delete_company/',views.delete_company,name='delete_company'),

]