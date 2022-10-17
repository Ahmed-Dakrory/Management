from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render,redirect,reverse
from django.core.exceptions import SuspiciousOperation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import json
from django.db.models import Count
from django.db.models import Sum
from django.db.models import Q
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models.query import QuerySet

from django.utils.translation import activate, get_language
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import HttpResponseRedirect
from django.http import HttpResponse 
from django.db import connection
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from datetime import datetime, timedelta,date

from mainApp.models import *

from io import StringIO
from io import BytesIO

import xlsxwriter
from django.http import HttpResponse




@login_required
def daily_report(request):
    
    show = False
    context = None
    if request.method=='POST':
        try:
            show = True
            day_to_generate = request.POST['day_to_generate']
            if day_to_generate!=None and day_to_generate!='':
                all_category = category.objects.filter( Q(deleted_date=None))
                all_size = size.objects.filter( Q(deleted_date=None))
                companies = company.objects.filter( Q(deleted_date=None))
                representatives = User.objects.filter( Q(deleted=None) ,Q(role__id=2))
                factories = factory.objects.filter( Q(deleted_date=None))

                total_in = companies.count()
                total_out = representatives.count()+factories.count()
                total = total_in+total_out
                context = {
                    'all_category':all_category,
                    'all_size':all_size,
                    'day_to_generate':day_to_generate,
                    'total_in':total_in,
                    'total_out':total_out,
                    'total':total,
                    'companies':companies,
                    'representatives':representatives,
                    'factories':factories,
                    'show':show,
                }
            else:
                show = False
                context = None

        except Exception as ee:
            print(ee)
            show = False
            context = None
            
            

    return render (request, 'reports/daily_report.html', context)





def export_daily_report(request):
    day_to_generate = request.POST['day_to_generate']
    
    day_to_generate = datetime.strptime(day_to_generate, '%d/%m/%Y')
    # print(day_to_generate)

    
     # create our spreadsheet.  I will create it in memory with a StringIO
    # output = StringIO()
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    all_category = category.objects.filter( Q(deleted_date=None))
    all_size = size.objects.filter( Q(deleted_date=None))
    i_row = 0
    

    size_format = workbook.add_format({
    'bold': True,
    'border': False,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#e8e8e8'})

    in_out_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#e8e8e8'})
    in_out_format.set_bottom(6)
    in_out_format.set_top(2)
    in_out_format.set_right(2)
    in_out_format.set_left(2)


    in_v_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#FFFFFF'})
    in_out_format.set_bottom(1)
    in_out_format.set_top(1)
    in_out_format.set_right(1)
    in_out_format.set_left(1)


    out_v_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#e8e8e8'})
    in_out_format.set_bottom(1)
    in_out_format.set_top(1)
    in_out_format.set_right(1)
    in_out_format.set_left(1)

   
    totalHead_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#e8e8e8'})
    totalHead_format.set_bottom(6)
    totalHead_format.set_top(6)
    totalHead_format.set_right(6)
    totalHead_format.set_left(6)
    totalHead_format.set_border(style=2)


    totalValue_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#24ffeb'})
    totalValue_format.set_border(style=2)

    model_format = workbook.add_format({
    'bold': True,
    'border': False,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#2493ff'})
    
    model_format.set_bottom(8)
    model_format.set_top(8)
    model_format.set_right(8)
    model_format.set_left(8)
    model_format.set_border(style=2)

    
    worksheet.merge_range('B1:AH4', "الجرد اليومى", out_v_format)

    worksheet.write(5,0, "Model")
    for row in all_category:
        worksheet.write(6+i_row,0, str(row.serial_start),model_format)
        j_col = 0
        for col in all_size:
            
            # Merge 3 cells.
            worksheet.merge_range(4,(3*j_col+1),4,(3*j_col+2), str(col.code), size_format)
            
            
            worksheet.write(5,(3*j_col+1), "IN",in_out_format)
            worksheet.write(5,(3*j_col+2), "OUT",in_out_format)
            worksheet.merge_range(4,(3*j_col+3),5,(3*j_col+3), "Total", totalHead_format)
            # 0 ==> 1
            # 1 ==> 4
            # 2 ==> 7
            # i ==> 3*i+1
            

            
            with connection.cursor() as cursorLast:
                try:
                    sql_query = """
                        SELECT count(distinct(item.id)) FROM management.transaction 
                        left join item on transaction.item_id=item.id
                        left join size on item.size_id=size.id
                        left join category on item.category_id=category.id
                        where category.id="""+str(row.id)+""" and size.id = """+str(col.id)+""" and ( type_of_transaction_id="""+str(settings.ID_ADD_TYPE_OF_TRANSACTION)+"""  or type_of_transaction_id="""+str(settings.ID_RETURN_TYPE_OF_TRANSACTION)+""")
                        and DATE_FORMAT(STR_TO_DATE(`item`.`created`, '%Y-%m-%d'), '%d-%m') = DATE_FORMAT(STR_TO_DATE('"""+str(day_to_generate.year)+"""-"""+str(day_to_generate.month)+"""-"""+str(day_to_generate.day)+"""','%Y-%m-%d'), '%d-%m')

                    """
                    # print(sql_query)
                    cursorLast.execute(sql_query)
                    cursorAllData = cursorLast.fetchone()
                    in_items=cursorAllData[0]
                except:
                    in_items = 0
                # print(in_items)
                try:
                    sql_query = """
                        SELECT count(distinct(item.id)) FROM management.transaction 
                        left join item on transaction.item_id=item.id
                        left join size on item.size_id=size.id
                        left join category on item.category_id=category.id
                        where category.id="""+str(row.id)+""" and size.id = """+str(col.id)+""" and ( type_of_transaction_id="""+str(settings.ID_OUT_TYPE_OF_TRANSACTION)+""")
                        and DATE_FORMAT(STR_TO_DATE(`item`.`created`, '%Y-%m-%d'), '%d-%m') = DATE_FORMAT(STR_TO_DATE('"""+str(day_to_generate.year)+"""-"""+str(day_to_generate.month)+"""-"""+str(day_to_generate.day)+"""','%Y-%m-%d'), '%d-%m')

                    """
                    # print(sql_query)
                    cursorLast.execute(sql_query)
                    cursorAllData = cursorLast.fetchone()
                    out_items=cursorAllData[0]
                except:
                    out_items = 0

            
                # except:
                #     pass
            # print("---------------------")
            # print(in_items)
            # for ii in in_items:
            #     print(ii.total)
            # print(out_items.total)
            # 16	3	13

            worksheet.write(6+i_row,(3*j_col+1), str(in_items),in_v_format)
            worksheet.write(6+i_row,(3*j_col+2), str(out_items),out_v_format)
            worksheet.write(6+i_row,(3*j_col+3), str(in_items-out_items),totalValue_format)
            j_col = j_col + 1

        i_row = i_row + 1
            
    workbook.close()

    # create a response
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="Report.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response

@login_required
def total_report(request):
    
    show = False
    context = None
    if request.method=='GET':
        try:
            show = True
            
            all_category = category.objects.filter( Q(deleted_date=None))
            all_size = size.objects.filter( Q(deleted_date=None))
            


            context = {
                'all_category':all_category,
                'all_size':all_size,
                'show':show,
            }
          

        except Exception as ee:
            print(ee)
            show = False
            context = None
            
            

    return render (request, 'reports/total_report.html', context)





def export_total_report(request):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    all_category = category.objects.filter( Q(deleted_date=None))
    all_size = size.objects.filter( Q(deleted_date=None))
    
    

    size_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#e8e8e8'})

    out_v_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#e8e8e8'})
    out_v_format.set_bottom(2)
    out_v_format.set_top(2)
    out_v_format.set_right(2)
    out_v_format.set_left(2)


    in_v_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#FFFFFF'})
    in_v_format.set_bottom(1)
    in_v_format.set_top(1)
    in_v_format.set_right(1)
    in_v_format.set_left(1)


    main_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#FFFFFF'})
    main_format.set_bottom(1)
    main_format.set_top(1)
    main_format.set_right(1)
    main_format.set_left(1)

   
    
    total_all_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#e8e8e8'})
    total_all_format.set_bottom(6)
    total_all_format.set_top(6)
    total_all_format.set_right(6)
    total_all_format.set_left(6)



    total_all_v_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#FFFFFF'})
    total_all_v_format.set_bottom(6)
    total_all_v_format.set_top(6)
    total_all_v_format.set_right(6)
    total_all_v_format.set_left(6)


    total_v_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#FFFFFF'})
    total_v_format.set_border(style=2)

    model_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#1346be'})
    
    model_format.set_bottom(8)
    model_format.set_top(8)
    model_format.set_right(8)
    model_format.set_left(8)
    model_format.set_border(style=2)

    
    worksheet.merge_range('B2:S3', "رصيد المخزن الفعلى", out_v_format)

    worksheet.merge_range('A5:C5', "Size -Code",out_v_format)
    i_row = 0
    for row in all_category:
        worksheet.write(5+i_row,0, str(i_row+1),main_format)
        worksheet.write(5+i_row,1, str(row.name),main_format)
        worksheet.write(5+i_row,2, str(row.serial_start),model_format)

        j_col = 0
        for col in all_size:
            
            # Merge 3 cells.
            worksheet.write(4,(j_col+3), str(col.code), size_format)
            
            
            # 0 ==> 1
            # 1 ==> 4
            # 2 ==> 7
            # i ==> 3*i+1
            
            total_items = item.objects.filter( Q(category__id=row.id) & Q(size__id=col.id) ).count()
            
            worksheet.write(5+i_row,(j_col+3), str(total_items),total_v_format)
            j_col = j_col + 1

        total_items = item.objects.filter( Q(category__id=row.id)).count()
        worksheet.write(5+i_row,(j_col+3), str(total_items),total_all_v_format)
        worksheet.write(4,(j_col+3), "SUM",total_all_format)
            

        i_row = i_row + 1
            
    workbook.close()

    # create a response
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="Report.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response




def factory_needed_report(request):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    all_category = category.objects.filter( Q(deleted_date=None))
    all_size = size.objects.filter( Q(deleted_date=None))
    
    

    size_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#e8e8e8'})

    out_v_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#e8e8e8'})
    out_v_format.set_bottom(2)
    out_v_format.set_top(2)
    out_v_format.set_right(2)
    out_v_format.set_left(2)


    in_v_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#FFFFFF'})
    in_v_format.set_bottom(1)
    in_v_format.set_top(1)
    in_v_format.set_right(1)
    in_v_format.set_left(1)


    main_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#FFFFFF'})
    main_format.set_bottom(1)
    main_format.set_top(1)
    main_format.set_right(1)
    main_format.set_left(1)

   
    
    total_all_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#e8e8e8'})
    total_all_format.set_bottom(6)
    total_all_format.set_top(6)
    total_all_format.set_right(6)
    total_all_format.set_left(6)



    total_all_v_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#FFFFFF'})
    total_all_v_format.set_bottom(6)
    total_all_v_format.set_top(6)
    total_all_v_format.set_right(6)
    total_all_v_format.set_left(6)


    total_v_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#FFFFFF'})
    total_v_format.set_border(style=2)

    model_format = workbook.add_format({
    'bold': True,
    'border': True,
    'align': 'center',
    'valign': 'vcenter',
    'fg_color': '#1346be'})
    
    model_format.set_bottom(8)
    model_format.set_top(8)
    model_format.set_right(8)
    model_format.set_left(8)
    model_format.set_border(style=2)

    
    worksheet.merge_range('F2:P2', "طليبة المصنع حسب الشريحة والعدد ", out_v_format)

    worksheet.merge_range('A5:D5', "Size -Code",out_v_format)
    i_row = 0
    for row in all_category:
        worksheet.write(5+i_row,0, str(i_row+1),main_format)
        worksheet.write(5+i_row,1, str(row.name),main_format)
        worksheet.write(5+i_row,2, str(row.color.name),main_format)
        worksheet.write(5+i_row,3, str(row.serial_start),model_format)

        j_col = 0
        needed_comulitve = 0
        for col in all_size:
            
            # Merge 3 cells.
            worksheet.write(4,(j_col+4), str(col.code), size_format)
            
            
            # 0 ==> 1
            # 1 ==> 4
            # 2 ==> 7
            # i ==> 3*i+1
            
            total_items = item.objects.filter( Q(category__id=row.id) & Q(size__id=col.id) & Q(exists=True) ).count()
            recommended_number_count = recommended_number.objects.filter(Q(category__id=row.id) & Q(size__id=col.id))[0].number
            

            needed =recommended_number_count-total_items
            if needed < 0:
                needed = 0
            
            needed_comulitve+=needed
            worksheet.write(5+i_row,(j_col+4), str(needed),total_v_format)
            j_col = j_col + 1

        # total_items = item.objects.filter( Q(category__id=row.id) & Q(exists=True)).count()
        # recommended_number_count = recommended_number.objects.filter(Q(category__id=row.id)).aggregate(Sum('number'))['number__sum']
        # print(str(recommended_number_count))
        # needed =recommended_number_count-total_items
        # if needed < 0:
        #     needed = 0
        worksheet.write(5+i_row,(j_col+4), str(needed_comulitve),total_all_v_format)
        worksheet.write(4,(j_col+4), "SUM",total_all_format)
            

        i_row = i_row + 1
            
    workbook.close()

    # create a response
    response = HttpResponse(content_type='application/vnd.ms-excel')

    # tell the browser what the file is named
    response['Content-Disposition'] = 'attachment;filename="Report.xlsx"'

    # put the spreadsheet data into the response
    response.write(output.getvalue())

    # return the response
    return response
