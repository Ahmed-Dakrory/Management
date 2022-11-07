from django.shortcuts import get_object_or_404
from django.http import Http404
from django.shortcuts import render,redirect,reverse
from django.core.exceptions import SuspiciousOperation
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
import json
from django.db.models import Count
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
import xlsxwriter
from django.http import HttpResponse


@login_required
def home(request):


    urlLink = reverse("mainApp:listOf_item")
    return redirect(urlLink)
    




@login_required
def show_companies(request):
    context = {
        
    }
    return render (request, 'elements/show_companies.html', context)

@login_required
def out_stock_item(request):
    all_color = color.objects.filter( Q(deleted_date=None))
    all_size = size.objects.filter( Q(deleted_date=None))
    all_company = company.objects.filter( Q(deleted_date=None))
    all_rep = User.objects.filter( Q(deleted=None) ,Q(role__id=2))
    

    if request.method=='POST':
        
        try:
            company_withObject = request.POST['company_with']
            company_withObject = company.objects.get(id=company_withObject)
        except:
            company_withObject = None
        

        try:
            representitive_withObject = request.POST['representitive_with']
            representitive_withObject = User.objects.get(id=representitive_withObject)
        except:
            representitive_withObject = None


        jsonArray_part_num = request.POST['jsonArray_part_num']
        
        all_parts = json.loads(jsonArray_part_num)
        for part_num in all_parts:
            # print(part_num)
            try:
                filedetails = request.FILES['file_'+str(part_num)]
                attachmentTranscriptObject = attachmentTranscript.objects.create(file = filedetails,content_type=filedetails.content_type,name=filedetails.name,table_name="transaction")
                attachmentTranscriptObject.save()
            except:
                attachmentTranscriptObject = None
            
            try:
                note = request.POST['note_'+str(part_num)]
            except:
                note = None
            
            itemObject = item.objects.filter(Q(part_num=part_num) & Q(exists=True))
            if itemObject is not None and len(itemObject)>0:
                # print("create")
                itemObject.update(last_out_date=datetime.now(),company_with=company_withObject,representitive_with=representitive_withObject,exists=False,is_returned=False)
                itemnew = item.objects.get(part_num=part_num)
                

                # print("create")
                type_of_transaction_object = type_of_transaction.objects.get(id=settings.ID_OUT_TYPE_OF_TRANSACTION)
                    
                # print("create")
                transactionObject = transaction.objects.create(
                    item = itemnew,
                    type_of_transaction = type_of_transaction_object,
                    image = attachmentTranscriptObject,
                    company = company_withObject,
                    representitive = representitive_withObject,
                    note = note
                )
                transactionObject.save()
                # print("create")

            
        
        

    context = {
        'all_company':all_company,
        'all_color':all_color,
        'all_size':all_size,
        'all_rep':all_rep
        }

    return render (request, 'operations/out_stock_item.html', context)




@login_required
def return_stock_item(request):

    all_color = color.objects.filter( Q(deleted_date=None))
    all_size = size.objects.filter( Q(deleted_date=None))
    all_company = company.objects.filter( Q(deleted_date=None))
    all_rep = User.objects.filter( Q(deleted=None) ,Q(role__id=2))
    

    if request.method=='POST':
        
        # try:
        #     company_withObject = request.POST['company_with']
        #     company_withObject = company.objects.get(id=company_withObject)
        # except:
        #     company_withObject = None
        

        # try:
        #     representitive_withObject = request.POST['representitive_with']
        #     representitive_withObject = User.objects.get(id=representitive_withObject)
        # except:
        #     representitive_withObject = None


        jsonArray_part_num = request.POST['jsonArray_part_num']
        
        all_parts = json.loads(jsonArray_part_num)
        for part_num in all_parts:
            # print(part_num)
            try:
                filedetails = request.FILES['file_'+str(part_num)]
                attachmentTranscriptObject = attachmentTranscript.objects.create(file = filedetails,content_type=filedetails.content_type,name=filedetails.name,table_name="transaction")
                attachmentTranscriptObject.save()
            except:
                attachmentTranscriptObject = None
            
            try:
                note = request.POST['note_'+str(part_num)]
            except:
                note = None
            
            itemObject = item.objects.filter(Q(part_num=part_num) & Q(exists=False))
            if itemObject is not None and len(itemObject)>0:
                # print("create")
                itemnew = item.objects.get(part_num=part_num)
                try:
                    representitive_withObject = itemnew.representitive_with
                except:
                    representitive_withObject = None

                try:
                    company_withObject = itemnew.company_with
                except:
                    company_withObject = None
                # print("create")
                type_of_transaction_object = type_of_transaction.objects.get(id=settings.ID_RETURN_TYPE_OF_TRANSACTION)
                    
                # print("create")
                transactionObject = transaction.objects.create(
                    item = itemnew,
                    type_of_transaction = type_of_transaction_object,
                    image = attachmentTranscriptObject,
                    company = company_withObject,
                    representitive = representitive_withObject,
                    note = note
                )
                transactionObject.save()
                
                
                itemObject.update(company_with=None,representitive_with=None,last_return_date=datetime.now(),exists=True,is_returned=True)
                
                

    context = {
        'all_company':all_company,
        'all_color':all_color,
        'all_size':all_size,
        'all_rep':all_rep
        }

    return render (request, 'operations/return_stock_item.html', context)








####################  category  #################3
@login_required
def listOf_category(request):
    
    return render(request,'category/list.html',None)


@login_required
def getListOf_category(request):
    pageLength = int(request.GET['length'])
    pageNumber = int(request.GET['start'])
    draw = int(request.GET['draw'])
    searchKey = request.GET['search[value]']
    pageNumber = int(pageNumber/pageLength + 1)
    
    try:
        if searchKey == '':
            allElements = category.objects.filter( Q(deleted_date=None))
        else:
            allElements = category.objects.filter(Q(deleted_date=None) & 
            (Q(name__contains=searchKey) |
             Q(name_en__contains=searchKey)|
             Q(color__name__contains=searchKey)|
             Q(color__name_en__contains=searchKey)|
             Q(factory__name__contains=searchKey)|
             Q(factory__name_en__contains=searchKey)|
             Q(serial_start__contains=searchKey)|
             Q(id__contains=searchKey) ))

        paginator = Paginator(allElements, pageLength)
        
        try:
            response = paginator.page(pageNumber)
        except PageNotAnInteger:
            response = paginator.page(pageNumber)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        listResult = list(response)
        allElementsJson = {"draw": draw,"recordsTotal": len(allElements),"recordsFiltered": len(allElements),"data":[]}

        for result in listResult:
            allElementsJson['data'].append(result.to_json())

        return JsonResponse(allElementsJson)
    except Exception as e:
        print("Ahmed Error: "+str(e))
        return JsonResponse({"draw": draw,"recordsTotal": 0,"recordsFiltered": 0,"data":[]})


@login_required
def addnew_category(request):
    typeOfEntry = request.GET['type']
    if typeOfEntry == 'new':
        dataToInsert = None
    elif typeOfEntry == 'edit':
        idOfelement = request.GET['id']
        dataToInsert = category.objects.get(id=idOfelement)
        
    
    
    all_factory = factory.objects.filter( Q(deleted_date=None))
    all_tranche = tranche.objects.filter( Q(deleted_date=None))
    all_color = color.objects.filter( Q(deleted_date=None))
    all_size = size.objects.filter( Q(deleted_date=None))
    
    
    context = {
        'categoryData':dataToInsert,
        'type':typeOfEntry,
        'all_factory':all_factory,
        'all_tranche':all_tranche,
        'all_color':all_color,
        'all_size':all_size
        }


    if request.method=='POST':
        name = request.POST['name']
        name_en = request.POST['name_en']
        year = request.POST['year']
        serial_start = request.POST['serial_start']
        colorObject = request.POST['color']
        details = request.POST['details']
        factoryObject = request.POST['factory']
        trancheObject = request.POST['tranche']

        try:
            factoryObject = factory.objects.get(id=factoryObject)
        except:
            factoryObject = None


        try:
            trancheObject = tranche.objects.get(id=trancheObject)
        except:
            trancheObject = None


        
        try:
            colorObject = color.objects.get(id=colorObject)
        except:
            colorObject = None

        
        

        try:
            filedetails = request.FILES['image']

        except Exception as err:
            print("----------------------")
            print(err)
            if typeOfEntry == 'edit':
                filedetails = dataToInsert.image.file
            else:
                filedetails = None
        if filedetails is None or filedetails == "":
            try:
                filedetails = dataToInsert.image.file
            except:
                filedetails = None

        # print("----------------------------------")
        # print(filedetails)




        if typeOfEntry == 'new':
            try:
                attachmentTranscriptObject = attachmentTranscript.objects.create(file = filedetails,content_type=filedetails.content_type,name=filedetails.name,table_name="category")
                attachmentTranscriptObject.save()
            except:
                attachmentTranscriptObject = None

            categorynew = category.objects.create(name=name,name_en=name_en,details=details,serial_start=serial_start,year=year, tranche=trancheObject,factory=factoryObject,color=colorObject,  created_by=request.user,image=attachmentTranscriptObject)
            categorynew.save()
            
            
        elif typeOfEntry == 'edit':
            try:
                attachmentTranscriptObject = attachmentTranscript.objects.create(file = filedetails,content_type=filedetails.content_type,name=filedetails.name,table_name="category")
                attachmentTranscriptObject.save()
            except Exception as err:
                print(err)
                print("----------------------")
                attachmentTranscriptObject = dataToInsert.image

            dataToInsert = category.objects.filter(id=idOfelement)
            dataToInsert.update(name=name,name_en=name_en,details=details,serial_start=serial_start,year=year, tranche=trancheObject, factory=factoryObject,color=colorObject,  updated_by=request.user,updated_date=datetime.now(),image=attachmentTranscriptObject)
            
            categorynew = category.objects.get(id=idOfelement)

        
        urlLink = reverse("mainApp:listOf_category")
        return redirect(urlLink)
    elif request.method=='GET':
        return render(request,'category/addnew.html',context)
    


@login_required
def delete_category(request):
    categoryId = request.POST['id']


    categoryDetails=category.objects.filter(Q(id=categoryId) & Q(deleted_date=None))
    categoryDetails.update(deleted_date = datetime.now())



   
    allJson = {"Result": "Fail"}
    
    allJson['Result'] = "Success"


    if allJson != None:
        return JsonResponse(allJson, safe=False)
    else:
        allJson['Result'] = "Fail"
        return JsonResponse(allJson, safe=False)
    



def get_all_categories_by_name(request):
    try:
        name = request.POST['name']
        all_category = category.objects.filter(Q(name=name) & Q(deleted_date=None))

        all_category = list(all_category)
        all_category_json = []
        for item in all_category:
            all_category_json.append(item.to_json())

        data = {"Result": "Success",'Data':all_category_json}
        # print(data)
        return JsonResponse(data)

    except:
        return JsonResponse({"Result": "Fail"})


####################  item  #################3
@login_required
def listOf_item(request):
    all_company = company.objects.filter( Q(deleted_date=None))
    all_rep = User.objects.filter( Q(deleted=None) ,Q(role__id=2))
    all_category = category.objects.filter( Q(deleted_date=None))
    all_size = size.objects.filter( Q(deleted_date=None))
    all_sector = sector.objects.filter( Q(deleted_date=None))

    all_category_group = category.objects.values('name').annotate(dcount=Count('name'))
    # for item in all_category_group:
    #     print(item)
    

    
    if request.method=='POST':
        for item_size in all_size:
            details = request.POST['details']

            try:
                number = request.POST['size_'+str(item_size.id)]
                sizeObject = size.objects.get(id=item_size.id)
            except Exception as err:
                # print(err)
                number = 0
                sizeObject = None

            if number != 0:
                try:
                    sectorObject = request.POST['sector_object']
                    sectorObject = sector.objects.get(id=sectorObject)
                except:
                    sectorObject = None

                try:
                    categoryId = request.POST['category_add']
                    categoryObject = category.objects.get(id=categoryId)
                except:
                    categoryObject = None

                # print("-----------------------")
                # print(number)
                for i in range(0,int(number)):
                    [part_num,higher_count] = generate_part_num(categoryObject,sizeObject)
                
                    itemnew = item.objects.create(part_num=part_num,
                    exists=True,
                    is_returned=False,
                    details=details,
                    sector = sectorObject,
                    company_with=None,
                    representitive_with=None,
                    category=categoryObject,
                    size=sizeObject,
                    higher_count = higher_count,
                    last_out_date=None,
                    last_return_date = None,
                    created_by=request.user)
                    itemnew.save()

                    type_of_transaction_object = type_of_transaction.objects.get(id=settings.ID_ADD_TYPE_OF_TRANSACTION)
                    
                    transactionObject = transaction.objects.create(
                        item = itemnew,
                        type_of_transaction = type_of_transaction_object,
                        note = ''
                    )
                    transactionObject.save()
                    

    context = {
        'all_company':all_company,
        'all_rep':all_rep,
        'all_category':all_category,
        'all_size':all_size,
        'all_sector':all_sector,
        'all_category_group':all_category_group
        }


    return render(request,'item/list.html',context)

@login_required
def item_by_part_num(request):
    pageLength = int(1)
    pageNumber = int(0)
    part_num = request.GET['part_num']
    draw = int(1)
    searchKey = ''
    # pageNumber = int(pageNumber/pageLength)

  
    
    with connection.cursor() as cursorLast:
        try:
            
           
            add_part_num = 'item.part_num = "'+str(part_num)+'"'

            sql_query = """



                    select concat('{"draw":\""""+str(draw)+"""\","recordsFiltered":',(select count(*) from item
                    left join category on item.category_id=category.id
                    left join size on item.size_id=size.id
                    left join color on category.color_id=color.id
                    left join company on item.company_with_id=company.id
                    left join attachmenttranscript on category.image_id=attachmenttranscript.id
                    left join factory on category.factory_id=factory.id
                    left join userapp_user on item.representitive_with_id=userapp_user.id
                    where item.deleted_date is null and
                    
                        """+add_part_num+""" 

                    
                    ),',
                    "recordsTotal":',count(*),',
                    "data":[',group_concat(concat('
                    {"id":',x.id,'
                    ,"part_num":"',x.part_num,'"
                    ,"color_name":"',x.color_name,'"
                    ,"color_name_en":"',x.color_name_en,'"
                    ,"size":"',x.size,'"
                    ,"size_code":"',x.size_code,'"
                    ,"factory_name":"',x.factory_name,'"
                    ,"factory_name_en":"',x.factory_name_en,'"
                    ,"company_with_name":"',x.company_with_name,'"
                    ,"company_with_name_en":"',x.company_with_name_en,'"
                    ,"representitive_with_name":"',x.representitive_with_name,'"
                    ,"representitive_with_phone":"',x.representitive_with_phone,'"
                    ,"last_out_date":"',x.last_out_date,'"
                    ,"last_return_date":"',x.last_return_date,'"
                    ,"details":"',x.details,'"
                    ,"exists":"',x.isexists,'"
                    ,"is_returned":"',x.is_returned,'"
                    ,"image":"',x.image,'"
                    ,"created":"',x.created,'"}
                    ')),']}')
                    as output
                    from (
                    SELECT  item.id as id,
                    IFNULL(part_num,"") as part_num,
                    IFNULL(color.name,"") as color_name,IFNULL(color.name_en,"") as color_name_en,
                    IFNULL(size.size,"") as size,IFNULL(size.code,"") as size_code,
                    IFNULL(factory.name,"") as factory_name,IFNULL(factory.name_en,"") as factory_name_en,
                    IFNULL(company.name,"") as company_with_name,IFNULL(company.name_en,"") as company_with_name_en,
                    IFNULL(userapp_user.username,"") as representitive_with_name,IFNULL(userapp_user.phone,"") as representitive_with_phone,
                    IFNULL(item.last_out_date,"") as last_out_date,IFNULL(item.last_return_date,"") as last_return_date,IFNULL(item.details,"") as details,IFNULL(item.exists,"") as isexists,IFNULL(item.is_returned,"") as is_returned,
                    IFNULL(attachmenttranscript.file,"") as image,
                    IFNULL(item.created,"") as created
                    FROM item
                    left join category on item.category_id=category.id
                    left join size on item.size_id=size.id
                    left join color on category.color_id=color.id
                    left join company on item.company_with_id=company.id
                    left join attachmenttranscript on category.image_id=attachmenttranscript.id
                    left join factory on category.factory_id=factory.id
                    left join userapp_user on item.representitive_with_id=userapp_user.id
                    where item.deleted_date is null
                    and (
                        """+add_part_num+""" 

                    )
                    order by item.created desc
                    LIMIT """+str(pageLength)+""" OFFSET """+str(pageNumber)+"""
                    ) x;

            """

                


               
            # print(sql_query)
            cursorLast.execute(sql_query)
            cursorAllData = cursorLast.fetchone()
            y=cursorAllData[0].replace('\r\n','')
            # print(y)
            return HttpResponse(y,content_type='application/json')

            
        except Exception as e:
            print("Ahmed Error: "+str(e))
            return JsonResponse({"draw": draw,"recordsTotal": 0,"recordsFiltered": 0,"data":[]})




@login_required
def getListOf_item(request):
    pageLength = int(request.GET['length'])
    pageNumber = int(request.GET['start'])
    draw = int(request.GET['draw'])
    searchKey = request.GET['search[value]']
    # pageNumber = int(pageNumber/pageLength)

    
    start_added_date = (request.GET['start_added_date'])
    end_added_date = (request.GET['end_added_date'])
    try:
        start_added_date = datetime.strptime(start_added_date, '%d/%m/%Y %H:%M')
        end_added_date = datetime.strptime(end_added_date, '%d/%m/%Y %H:%M')

        start_added_date = start_added_date.strftime("%Y-%m-%d %H:%M:%S")
        end_added_date = end_added_date.strftime("%Y-%m-%d %H:%M:%S")
        created_search = " and item.created>='"+start_added_date+"' and item.created<='"+end_added_date+"' "
    except:
        created_search = "  "

    # print("-----------------------------------------")
    # print(start_added_date)
    # print(end_added_date)
    
    category = (request.GET['category'])
    if category == '%%':
        category_search = ' item.deleted_date is null '
    else:
        category_search = ' category.id='+str(category)+' '


    sector = (request.GET['sector'])
    if sector == '%%':
        sector_search = ' item.deleted_date is null '
    else:
        sector_search = ' sector.id='+str(sector)+' '


    

    company_with = (request.GET['company_with'])
    if company_with == '%%':
        company_with_search = ' item.deleted_date is null '
    else:
        company_with_search = ' company.id='+str(company_with)+' '

    size = (request.GET['size'])
    if size == '%%':
        size_search = ' item.deleted_date is null '
    else:
        size_search = ' size.id='+str(size)+' '

    representitive_with = (request.GET['representitive_with'])
    if representitive_with == '%%':
        representitive_with_search = ' item.deleted_date is null '
    else:
        representitive_with_search = ' userapp_user.id='+str(representitive_with)+' '


    
    exists = (request.GET['exists'])
    if exists == '%%':
        exists_search = ' item.deleted_date is null '
    else:
        exists_search = ' item.exists='+str(exists)+' '

    with connection.cursor() as cursorLast:
        try:
            if searchKey == '':
                sql_query = """



                        select concat('{"draw":\""""+str(draw)+"""\","recordsFiltered":',(select count(*) from item
                        left join category on item.category_id=category.id
                        left join size on item.size_id=size.id
                        left join color on category.color_id=color.id
                        left join company on item.company_with_id=company.id
                        left join attachmenttranscript on category.image_id=attachmenttranscript.id
                        left join factory on category.factory_id=factory.id
                        left join userapp_user on item.representitive_with_id=userapp_user.id
                        where item.deleted_date is null
                        and """+exists_search+"""
                        and """+representitive_with_search+"""
                        and """+company_with_search+"""
                        and """+size_search+"""
                        and """+category_search+"""
                        and """+sector_search+"""
                            """+created_search+"""
                        
                        ),',
                        "recordsTotal":',count(*),',
                        "data":[',group_concat(concat('
                        {"id":',x.id,'
                        ,"part_num":"',x.part_num,'"
                        ,"color_name":"',x.color_name,'"
                        ,"color_name_en":"',x.color_name_en,'"
                        ,"size":"',x.size,'"
                        ,"size_code":"',x.size_code,'"
                        ,"factory_name":"',x.factory_name,'"
                        ,"factory_name_en":"',x.factory_name_en,'"
                        ,"company_with_name":"',x.company_with_name,'"
                        ,"company_with_name_en":"',x.company_with_name_en,'"
                        ,"representitive_with_name":"',x.representitive_with_name,'"
                        ,"representitive_with_phone":"',x.representitive_with_phone,'"
                        ,"last_out_date":"',x.last_out_date,'"
                        ,"last_return_date":"',x.last_return_date,'"
                        ,"details":"',x.details,'"
                        ,"exists":"',x.isexists,'"
                        ,"is_returned":"',x.is_returned,'"
                        ,"image":"',x.image,'"
                        ,"created":"',x.created,'"}
                        ')),']}')
                        as output
                        from (
                        SELECT  item.id as id,
                        IFNULL(part_num,"") as part_num,
                        IFNULL(color.name,"") as color_name,IFNULL(color.name_en,"") as color_name_en,
                        IFNULL(size.size,"") as size,IFNULL(size.code,"") as size_code,
                        IFNULL(factory.name,"") as factory_name,IFNULL(factory.name_en,"") as factory_name_en,
                        IFNULL(company.name,"") as company_with_name,IFNULL(company.name_en,"") as company_with_name_en,
                        IFNULL(userapp_user.username,"") as representitive_with_name,IFNULL(userapp_user.phone,"") as representitive_with_phone,
                        IFNULL(item.last_out_date,"") as last_out_date,IFNULL(item.last_return_date,"") as last_return_date,IFNULL(item.details,"") as details,IFNULL(item.exists,"") as isexists,IFNULL(item.is_returned,"") as is_returned,
                        IFNULL(attachmenttranscript.file,"") as image,
                        IFNULL(item.created,"") as created
                        FROM item
                        left join category on item.category_id=category.id
                        left join size on item.size_id=size.id
                        left join color on category.color_id=color.id
                        left join company on item.company_with_id=company.id
                        left join attachmenttranscript on category.image_id=attachmenttranscript.id
                        left join factory on category.factory_id=factory.id
                        left join userapp_user on item.representitive_with_id=userapp_user.id
                        where item.deleted_date is null
                        and """+exists_search+"""
                        and """+representitive_with_search+"""
                        and """+company_with_search+"""
                        and """+size_search+"""
                        and """+category_search+"""
                        and """+sector_search+"""
                            """+created_search+"""
                        order by item.created desc
                        LIMIT """+str(pageLength)+""" OFFSET """+str(pageNumber)+"""
                        ) x;

                """
            else:

                add_size_code = 'size.code like "%'+str(searchKey)+'%"'
                add_color__name = 'color.name like "%'+str(searchKey)+'%"'
                add_color__name_en = 'color.name_en like "%'+str(searchKey)+'%"'
                add_company_with__name = 'company.name like "%'+str(searchKey)+'%"'
                add_company_with__name_en = 'company.name_en like "%'+str(searchKey)+'%"'
                add_representitive_with__username = 'userapp_user.username like "%'+str(searchKey)+'%"'
                add_part_num = 'item.part_num like "%'+str(searchKey)+'%"'
                add_id = 'item.id like "%'+str(searchKey)+'%"'

                sql_query = """



                        select concat('{"draw":\""""+str(draw)+"""\","recordsFiltered":',(select count(*) from item
                        left join category on item.category_id=category.id
                        left join size on item.size_id=size.id
                        left join color on category.color_id=color.id
                        left join company on item.company_with_id=company.id
                        left join attachmenttranscript on category.image_id=attachmenttranscript.id
                        left join factory on category.factory_id=factory.id
                        left join userapp_user on item.representitive_with_id=userapp_user.id
                        where item.deleted_date is null
                        and """+exists_search+"""
                        and """+representitive_with_search+"""
                        and """+company_with_search+"""
                        and """+size_search+"""
                        and """+category_search+"""
                        and """+sector_search+"""
                            """+created_search+"""

                        and (
                            """+add_size_code+""" or 
                            """+add_color__name+""" or 
                            """+add_color__name_en+""" or 
                            """+add_company_with__name+""" or 
                            """+add_company_with__name_en+""" or 
                            """+add_representitive_with__username+""" or 
                            """+add_part_num+""" or 
                            """+add_id+""" 

                        )
                        ),',
                        "recordsTotal":',count(*),',
                        "data":[',group_concat(concat('
                        {"id":',x.id,'
                        ,"part_num":"',x.part_num,'"
                        ,"color_name":"',x.color_name,'"
                        ,"color_name_en":"',x.color_name_en,'"
                        ,"size":"',x.size,'"
                        ,"size_code":"',x.size_code,'"
                        ,"factory_name":"',x.factory_name,'"
                        ,"factory_name_en":"',x.factory_name_en,'"
                        ,"company_with_name":"',x.company_with_name,'"
                        ,"company_with_name_en":"',x.company_with_name_en,'"
                        ,"representitive_with_name":"',x.representitive_with_name,'"
                        ,"representitive_with_phone":"',x.representitive_with_phone,'"
                        ,"last_out_date":"',x.last_out_date,'"
                        ,"last_return_date":"',x.last_return_date,'"
                        ,"details":"',x.details,'"
                        ,"exists":"',x.isexists,'"
                        ,"is_returned":"',x.is_returned,'"
                        ,"image":"',x.image,'"
                        ,"created":"',x.created,'"}
                        ')),']}')
                        as output
                        from (
                        SELECT  item.id as id,
                        IFNULL(part_num,"") as part_num,
                        IFNULL(color.name,"") as color_name,IFNULL(color.name_en,"") as color_name_en,
                        IFNULL(size.size,"") as size,IFNULL(size.code,"") as size_code,
                        IFNULL(factory.name,"") as factory_name,IFNULL(factory.name_en,"") as factory_name_en,
                        IFNULL(company.name,"") as company_with_name,IFNULL(company.name_en,"") as company_with_name_en,
                        IFNULL(userapp_user.username,"") as representitive_with_name,IFNULL(userapp_user.phone,"") as representitive_with_phone,
                        IFNULL(item.last_out_date,"") as last_out_date,IFNULL(item.last_return_date,"") as last_return_date,IFNULL(item.details,"") as details,IFNULL(item.exists,"") as isexists,IFNULL(item.is_returned,"") as is_returned,
                        IFNULL(attachmenttranscript.file,"") as image,
                        IFNULL(item.created,"") as created
                        FROM item
                        left join category on item.category_id=category.id
                        left join size on item.size_id=size.id
                        left join color on category.color_id=color.id
                        left join company on item.company_with_id=company.id
                        left join attachmenttranscript on category.image_id=attachmenttranscript.id
                        left join factory on category.factory_id=factory.id
                        left join userapp_user on item.representitive_with_id=userapp_user.id
                        where item.deleted_date is null
                        and """+exists_search+"""
                        and """+representitive_with_search+"""
                        and """+company_with_search+"""
                        and """+size_search+"""
                        and """+category_search+"""
                        and """+sector_search+"""
                         """+created_search+"""

                        and (
                            """+add_size_code+""" or 
                            """+add_color__name+""" or 
                            """+add_color__name_en+""" or 
                            """+add_company_with__name+""" or 
                            """+add_company_with__name_en+""" or 
                            """+add_representitive_with__username+""" or 
                            """+add_part_num+""" or 
                            """+add_id+""" 

                        )
                        order by item.created desc
                        LIMIT """+str(pageLength)+""" OFFSET """+str(pageNumber)+"""
                        ) x;

                """

                


               
            # print(sql_query)
            cursorLast.execute(sql_query)
            cursorAllData = cursorLast.fetchone()
            y=cursorAllData[0].replace('\r\n','')
            # print(y)
            return HttpResponse(y,content_type='application/json')

            
        except Exception as e:
            print("Ahmed Error: "+str(e))
            return JsonResponse({"draw": draw,"recordsTotal": 0,"recordsFiltered": 0,"data":[]})


@login_required
def addnew_item(request):
    typeOfEntry = request.GET['type']
    if typeOfEntry == 'new':
        dataToInsert = None
    elif typeOfEntry == 'edit':
        idOfelement = request.GET['id']
        dataToInsert = item.objects.get(id=idOfelement)
    
    
    all_company = company.objects.filter( Q(deleted_date=None))
    all_rep = User.objects.filter( Q(deleted=None) ,Q(role__id=2))
    all_category = category.objects.filter( Q(deleted_date=None))
    all_size = size.objects.filter( Q(deleted_date=None))
    all_sector = sector.objects.filter( Q(deleted_date=None))

    context = {
        'itemData':dataToInsert,
        'type':typeOfEntry,
        'all_company':all_company,
        'all_rep':all_rep,
        'all_category':all_category,
        'all_size':all_size,
        'all_sector':all_sector
        }


    if request.method=='POST':
        # part_num = request.POST['part_num']
        exists = request.POST['exists']
        details = request.POST['details']
        is_returned = request.POST['is_returned']
        company_with = request.POST['company_with']
        sectorId = request.POST['sector']
        representitive_with = request.POST['representitive_with']
        last_out_date = request.POST['last_out_date']
        last_return_date = request.POST['last_return_date']

        try:
            last_out_date = datetime.strptime(last_out_date, '%d/%m/%Y %H:%M')
        except:
            last_out_date = None


        
        try:
            last_return_date = datetime.strptime(last_return_date, '%d/%m/%Y %H:%M')
        except:
            last_return_date = None

        if is_returned == '1':
            is_returned = True
        else: 
            is_returned = False

        if exists == '1':
            exists = True
        else: 
            exists = False

        try:
            companyObject = company.objects.get(id=company_with)
        except:
            companyObject = None


        try:
            sectorObject = sector.objects.get(id=sectorId)
        except:
            sectorObject = None

        

        
        try:
            sizeObject = request.POST['size']
            sizeObject = size.objects.get(id=sizeObject)
        except:
            sizeObject = None
        
        try:
            representitive_withObject = User.objects.get(id=representitive_with)
        except:
            representitive_withObject = None

        
        try:
            categoryId = request.POST['category']
            categoryObject = category.objects.get(id=categoryId)
        except:
            categoryObject = None

        
        



        if typeOfEntry == 'new':
            type_of_transaction_object = type_of_transaction.objects.get(id=settings.ID_ADD_TYPE_OF_TRANSACTION)
            
            [part_num,higher_count] = generate_part_num(categoryObject,sizeObject)
        
            itemnew = item.objects.create(part_num=part_num,
            exists=exists,
            is_returned=is_returned,
            details=details,
            company_with=companyObject,
            sector = sectorObject,
            representitive_with=representitive_withObject,
            category=categoryObject,
            size=sizeObject,
            higher_count = higher_count,
            last_out_date=last_out_date,
            last_return_date = last_return_date,
            created_by=request.user)
            itemnew.save()


            
            transactionObject = transaction.objects.create(
                item = itemnew,
                type_of_transaction = type_of_transaction_object,
                note = ''
            )
            transactionObject.save()
            
            
        elif typeOfEntry == 'edit':
            

            dataToInsert = item.objects.filter(id=idOfelement)
            dataToInsert.update(
            exists=exists,
            is_returned=is_returned,
            details=details,
            company_with=companyObject,
            sector = sectorObject,
            representitive_with=representitive_withObject,
            last_out_date=last_out_date,
            last_return_date = last_return_date,
            created_by=request.user,  updated_by=request.user,updated_date=datetime.now())
            

 
        urlLink = reverse("mainApp:listOf_item")
        return redirect(urlLink)
    elif request.method=='GET':
        return render(request,'item/addnew.html',context)
    


@login_required
def show_item(request):
    typeOfEntry = request.GET['type']
    if typeOfEntry == 'new':
        dataToInsert = None
    elif typeOfEntry == 'edit':
        idOfelement = request.GET['id']
        dataToInsert = item.objects.get(id=idOfelement)
    
    
    transactionObject = transaction.objects.filter(Q(item = dataToInsert))

    all_company = company.objects.filter( Q(deleted_date=None))
    all_rep = User.objects.filter( Q(deleted=None) ,Q(role__id=2))
    all_category = category.objects.filter( Q(deleted_date=None))
    all_size = size.objects.filter( Q(deleted_date=None))
    all_sector = sector.objects.filter( Q(deleted_date=None))

    context = {
        'itemData':dataToInsert,
        'type':typeOfEntry,
        'all_company':all_company,
        'all_rep':all_rep,
        'all_category':all_category,
        'all_size':all_size,
        'all_sector':all_sector,
        'transactionObject':transactionObject
        }


    return render(request,'item/view.html',context)
    


@login_required
def delete_item(request):
    itemId = request.POST['id']


    itemDetails=item.objects.filter(Q(id=itemId) & Q(deleted_date=None))
    itemDetails.update(deleted_date = datetime.now())



   
    allJson = {"Result": "Fail"}
    
    allJson['Result'] = "Success"


    if allJson != None:
        return JsonResponse(allJson, safe=False)
    else:
        allJson['Result'] = "Fail"
        return JsonResponse(allJson, safe=False)
    




####################  factory  #################3
@login_required
def listOf_factory(request):
    
    return render(request,'factory/list.html',None)


@login_required
def getListOf_factory(request):
    pageLength = int(request.GET['length'])
    pageNumber = int(request.GET['start'])
    draw = int(request.GET['draw'])
    searchKey = request.GET['search[value]']
    pageNumber = int(pageNumber/pageLength + 1)
    
    try:
        if searchKey == '':
            allElements = factory.objects.filter( Q(deleted_date=None))
        else:
            allElements = factory.objects.filter(Q(deleted_date=None) & 
            (Q(name__contains=searchKey) |
             Q(name_en__contains=searchKey)|
             Q(head_phone__contains=searchKey)|
             Q(factory_phone__contains=searchKey)|
             Q(tax_number__contains=searchKey)|
             Q(id__contains=searchKey) ))

        paginator = Paginator(allElements, pageLength)
        
        try:
            response = paginator.page(pageNumber)
        except PageNotAnInteger:
            response = paginator.page(pageNumber)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        listResult = list(response)
        allElementsJson = {"draw": draw,"recordsTotal": len(allElements),"recordsFiltered": len(allElements),"data":[]}

        for result in listResult:
            allElementsJson['data'].append(result.to_json())

        return JsonResponse(allElementsJson)
    except Exception as e:
        print("Ahmed Error: "+str(e))
        return JsonResponse({"draw": draw,"recordsTotal": 0,"recordsFiltered": 0,"data":[]})


@login_required
def addnew_factory(request):
    typeOfEntry = request.GET['type']
    if typeOfEntry == 'new':
        dataToInsert = None
    elif typeOfEntry == 'edit':
        idOfelement = request.GET['id']
        dataToInsert = factory.objects.get(id=idOfelement)
    
    
    context = {
        'factoryData':dataToInsert,
        'type':typeOfEntry
        }


    if request.method=='POST':
        name = request.POST['name']
        name_en = request.POST['name_en']
        head_phone = request.POST['head_phone']
        factory_phone = request.POST['factory_phone']
        tax_number = request.POST['tax_number']
        address = request.POST['address']
        
        try:
            filedetails = request.FILES['image']

        except Exception as err:
            print("----------------------")
            print(err)
            if typeOfEntry == 'edit':
                filedetails = dataToInsert.image.file
            else:
                filedetails = None
        
        if filedetails is None or filedetails == "":
            try:
                filedetails = dataToInsert.image.file
            except:
                filedetails = None



        if typeOfEntry == 'new':
            try:
                attachmentTranscriptObject = attachmentTranscript.objects.create(file = filedetails,content_type=filedetails.content_type,name=filedetails.name,table_name="factory")
                attachmentTranscriptObject.save()
            except:
                attachmentTranscriptObject = None

            factorynew = factory.objects.create(name=name,name_en=name_en,head_phone=head_phone, factory_phone=factory_phone,tax_number=tax_number,address=address,  created_by=request.user,image=attachmentTranscriptObject)
            factorynew.save()
            
            
        elif typeOfEntry == 'edit':
            try:
                attachmentTranscriptObject = attachmentTranscript.objects.create(file = filedetails,content_type=filedetails.content_type,name=filedetails.name,table_name="factory")
                attachmentTranscriptObject.save()
            except Exception as err:
                print(err)
                print("----------------------")
                attachmentTranscriptObject = dataToInsert.image

            dataToInsert = factory.objects.filter(id=idOfelement)
            dataToInsert.update(name=name,name_en=name_en,head_phone=head_phone, factory_phone=factory_phone,tax_number=tax_number,address=address,  updated_by=request.user,updated_date=datetime.now(),image=attachmentTranscriptObject)
            

 
        urlLink = reverse("mainApp:listOf_factory")
        return redirect(urlLink)
    elif request.method=='GET':
        return render(request,'factory/addnew.html',context)
    


@login_required
def delete_factory(request):
    factoryId = request.POST['id']


    factoryDetails=factory.objects.filter(Q(id=factoryId) & Q(deleted_date=None))
    factoryDetails.update(deleted_date = datetime.now())



   
    allJson = {"Result": "Fail"}
    
    allJson['Result'] = "Success"


    if allJson != None:
        return JsonResponse(allJson, safe=False)
    else:
        allJson['Result'] = "Fail"
        return JsonResponse(allJson, safe=False)
    






####################  tranche  #################3
@login_required
def listOf_tranche(request):
    
    return render(request,'tranche/list.html',None)


@login_required
def getListOf_tranche(request):
    pageLength = int(request.GET['length'])
    pageNumber = int(request.GET['start'])
    draw = int(request.GET['draw'])
    searchKey = request.GET['search[value]']
    pageNumber = int(pageNumber/pageLength + 1)
    
    try:
        if searchKey == '':
            allElements = tranche.objects.filter( Q(deleted_date=None))
        else:
            allElements = tranche.objects.filter(Q(deleted_date=None) & 
            (Q(name__contains=searchKey) |
             Q(name_en__contains=searchKey)|
             Q(id__contains=searchKey) ))

        paginator = Paginator(allElements, pageLength)
        
        try:
            response = paginator.page(pageNumber)
        except PageNotAnInteger:
            response = paginator.page(pageNumber)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        listResult = list(response)
        allElementsJson = {"draw": draw,"recordsTotal": len(allElements),"recordsFiltered": len(allElements),"data":[]}

        for result in listResult:
            allElementsJson['data'].append(result.to_json())

        return JsonResponse(allElementsJson)
    except Exception as e:
        print("Ahmed Error: "+str(e))
        return JsonResponse({"draw": draw,"recordsTotal": 0,"recordsFiltered": 0,"data":[]})


@login_required
def addnew_tranche(request):
    typeOfEntry = request.GET['type']
    all_size = size.objects.filter( Q(deleted_date=None))
    if typeOfEntry == 'new':
        dataToInsert = None
        recommended_numberObject_all = None
    elif typeOfEntry == 'edit':
        idOfelement = request.GET['id']
        dataToInsert = tranche.objects.get(id=idOfelement)
        recommended_numberObject_all = recommended_number.objects.filter( Q(tranche__id=idOfelement))
    
    
    context = {
        'trancheData':dataToInsert,
        'type':typeOfEntry,
        'recommended_numberObject_all':recommended_numberObject_all,
        'all_size':all_size
        }


    if request.method=='POST':
        name = request.POST['name']
        name_en = request.POST['name_en']
        
        
        if typeOfEntry == 'new':
            tranchenew = tranche.objects.create(name=name,name_en=name_en)
            tranchenew.save()
            
            
        elif typeOfEntry == 'edit':
            dataToInsert = tranche.objects.filter(id=idOfelement)
            dataToInsert.update(name=name,name_en=name_en,  updated_by=request.user,updated_date=datetime.now())
            
            tranchenew = tranche.objects.get(id=idOfelement)


        for key in request.POST:
            if 'size_' in key :
                size_code = key.split('_')[1]
                number = request.POST[key]
                size_object = size.objects.get(code = size_code)
                recommended_numberObject = recommended_number.objects.filter(Q(size__id=size_object.id)& Q(tranche__id=tranchenew.id))
                if recommended_numberObject is not None and len(recommended_numberObject)>0:
                    recommended_numberObject.update(
                        number=number,
                    )
                else:
                    recommended_numberObject = recommended_number.objects.create(
                        number=number,
                        tranche=tranchenew,
                        size = size_object
                    )
                    recommended_numberObject.save()
                
 
         

 
        urlLink = reverse("mainApp:listOf_tranche")
        return redirect(urlLink)
    elif request.method=='GET':
        return render(request,'tranche/addnew.html',context)
    


@login_required
def delete_tranche(request):
    trancheId = request.POST['id']


    trancheDetails=tranche.objects.filter(Q(id=trancheId) & Q(deleted_date=None))
    trancheDetails.update(deleted_date = datetime.now())



   
    allJson = {"Result": "Fail"}
    
    allJson['Result'] = "Success"


    if allJson != None:
        return JsonResponse(allJson, safe=False)
    else:
        allJson['Result'] = "Fail"
        return JsonResponse(allJson, safe=False)
    





####################  sector  #################3
@login_required
def listOf_sector(request):
    
    return render(request,'sector/list.html',None)


@login_required
def getListOf_sector(request):
    pageLength = int(request.GET['length'])
    pageNumber = int(request.GET['start'])
    draw = int(request.GET['draw'])
    searchKey = request.GET['search[value]']
    pageNumber = int(pageNumber/pageLength + 1)
    
    try:
        if searchKey == '':
            allElements = sector.objects.filter( Q(deleted_date=None))
        else:
            allElements = sector.objects.filter(Q(deleted_date=None) & 
            (Q(name__contains=searchKey) |
             Q(name_en__contains=searchKey)|
             Q(floor__contains=searchKey)|
             Q(id__contains=searchKey) ))

        paginator = Paginator(allElements, pageLength)
        
        try:
            response = paginator.page(pageNumber)
        except PageNotAnInteger:
            response = paginator.page(pageNumber)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        listResult = list(response)
        allElementsJson = {"draw": draw,"recordsTotal": len(allElements),"recordsFiltered": len(allElements),"data":[]}

        for result in listResult:
            allElementsJson['data'].append(result.to_json())

        return JsonResponse(allElementsJson)
    except Exception as e:
        print("Ahmed Error: "+str(e))
        return JsonResponse({"draw": draw,"recordsTotal": 0,"recordsFiltered": 0,"data":[]})


@login_required
def addnew_sector(request):
    typeOfEntry = request.GET['type']
    if typeOfEntry == 'new':
        dataToInsert = None
    elif typeOfEntry == 'edit':
        idOfelement = request.GET['id']
        dataToInsert = sector.objects.get(id=idOfelement)
    
    
    context = {
        'sectorData':dataToInsert,
        'type':typeOfEntry
        }


    if request.method=='POST':
        name = request.POST['name']
        name_en = request.POST['name_en']
        floor = request.POST['floor']
        
        try:
            filedetails = request.FILES['image']

        except Exception as err:
            print("----------------------")
            print(err)
            if typeOfEntry == 'edit':
                filedetails = dataToInsert.image.file
            else:
                filedetails = None

        if filedetails is None or filedetails == "":
            try:
                filedetails = dataToInsert.image.file
            except:
                filedetails = None



        if typeOfEntry == 'new':
            try:
                attachmentTranscriptObject = attachmentTranscript.objects.create(file = filedetails,content_type=filedetails.content_type,name=filedetails.name,table_name="sector")
                attachmentTranscriptObject.save()
            except:
                attachmentTranscriptObject = None

            sectornew = sector.objects.create(name=name,name_en=name_en,floor=floor,  created_by=request.user,image=attachmentTranscriptObject)
            sectornew.save()
            
            
        elif typeOfEntry == 'edit':
            try:
                attachmentTranscriptObject = attachmentTranscript.objects.create(file = filedetails,content_type=filedetails.content_type,name=filedetails.name,table_name="sector")
                attachmentTranscriptObject.save()
            except Exception as err:
                print(err)
                print("----------------------")
                attachmentTranscriptObject = dataToInsert.image

            dataToInsert = sector.objects.filter(id=idOfelement)
            dataToInsert.update(name=name,name_en=name_en,floor=floor,  updated_by=request.user,updated_date=datetime.now(),image=attachmentTranscriptObject)
            

 
        urlLink = reverse("mainApp:listOf_sector")
        return redirect(urlLink)
    elif request.method=='GET':
        return render(request,'sector/addnew.html',context)
    


@login_required
def delete_sector(request):
    sectorId = request.POST['id']


    sectorDetails=sector.objects.filter(Q(id=sectorId) & Q(deleted_date=None))
    sectorDetails.update(deleted_date = datetime.now())



   
    allJson = {"Result": "Fail"}
    
    allJson['Result'] = "Success"


    if allJson != None:
        return JsonResponse(allJson, safe=False)
    else:
        allJson['Result'] = "Fail"
        return JsonResponse(allJson, safe=False)
    





####################  company  #################3
@login_required
def listOf_company(request):
    
    return render(request,'company/list.html',None)


@login_required
def getListOf_company(request):
    pageLength = int(request.GET['length'])
    pageNumber = int(request.GET['start'])
    draw = int(request.GET['draw'])
    searchKey = request.GET['search[value]']
    pageNumber = int(pageNumber/pageLength + 1)
    
    try:
        if searchKey == '':
            allElements = company.objects.filter( Q(deleted_date=None))
        else:
            allElements = company.objects.filter(Q(deleted_date=None) & 
            (Q(name__contains=searchKey) |
             Q(name_en__contains=searchKey)|
             Q(head_phone__contains=searchKey)|
             Q(company_phone__contains=searchKey)|
             Q(tax_number__contains=searchKey)|
             Q(id__contains=searchKey) ))

        paginator = Paginator(allElements, pageLength)
        
        try:
            response = paginator.page(pageNumber)
        except PageNotAnInteger:
            response = paginator.page(pageNumber)
        except EmptyPage:
            response = paginator.page(paginator.num_pages)

        listResult = list(response)
        allElementsJson = {"draw": draw,"recordsTotal": len(allElements),"recordsFiltered": len(allElements),"data":[]}

        for result in listResult:
            allElementsJson['data'].append(result.to_json())

        return JsonResponse(allElementsJson)
    except Exception as e:
        print("Ahmed Error: "+str(e))
        return JsonResponse({"draw": draw,"recordsTotal": 0,"recordsFiltered": 0,"data":[]})


@login_required
def addnew_company(request):
    typeOfEntry = request.GET['type']
    if typeOfEntry == 'new':
        dataToInsert = None
    elif typeOfEntry == 'edit':
        idOfelement = request.GET['id']
        dataToInsert = company.objects.get(id=idOfelement)
    
    
    context = {
        'companyData':dataToInsert,
        'type':typeOfEntry
        }


    if request.method=='POST':
        name = request.POST['name']
        name_en = request.POST['name_en']
        head_phone = request.POST['head_phone']
        company_phone = request.POST['company_phone']
        tax_number = request.POST['tax_number']
        address = request.POST['address']

        try:
            filedetails = request.FILES['image']

        except Exception as err:
            print("----------------------")
            print(err)
            if typeOfEntry == 'edit':
                filedetails = dataToInsert.image.file
            else:
                filedetails = None

        if filedetails is None or filedetails == "":
            try:
                filedetails = dataToInsert.image.file
            except:
                filedetails = None
        



        if typeOfEntry == 'new':
            try:
                attachmentTranscriptObject = attachmentTranscript.objects.create(file = filedetails,content_type=filedetails.content_type,name=filedetails.name,table_name="company")
                attachmentTranscriptObject.save()
            except:
                attachmentTranscriptObject = None

            companynew = company.objects.create(name=name,name_en=name_en,head_phone=head_phone, company_phone=company_phone,tax_number=tax_number,address=address,  created_by=request.user,image=attachmentTranscriptObject)
            companynew.save()

            
        elif typeOfEntry == 'edit':
            try:
                attachmentTranscriptObject = attachmentTranscript.objects.create(file = filedetails,content_type=filedetails.content_type,name=filedetails.name,table_name="company")
                attachmentTranscriptObject.save()
            except Exception as err:
                print(err)
                print("----------------------")
                attachmentTranscriptObject = dataToInsert.image

            dataToInsert = company.objects.filter(id=idOfelement)
            dataToInsert.update(name=name,name_en=name_en,head_phone=head_phone, company_phone=company_phone,tax_number=tax_number,address=address,  updated_by=request.user,updated_date=datetime.now(),image=attachmentTranscriptObject)
            

 
        urlLink = reverse("mainApp:listOf_company")
        return redirect(urlLink)
    elif request.method=='GET':
        return render(request,'company/addnew.html',context)
    


@login_required
def delete_company(request):
    companyId = request.POST['id']


    companyDetails=company.objects.filter(Q(id=companyId) & Q(deleted_date=None))
    companyDetails.update(deleted_date = datetime.now())



   
    allJson = {"Result": "Fail"}
    
    allJson['Result'] = "Success"


    if allJson != None:
        return JsonResponse(allJson, safe=False)
    else:
        allJson['Result'] = "Fail"
        return JsonResponse(allJson, safe=False)
    



@login_required
def show_items(request):
    context = {
        
    }
    return render (request, 'elements/show_items.html', context)











def checkUniquenessOfpart_num(request):
    part_num = request.POST['part_num']
    id = request.POST['id']
    if id == '' or id == None:
        nameExists = item.objects.filter(part_num=part_num).exists()

    else:
        nameExists = item.objects.filter(part_num=part_num).exclude(id=id).exists()


    if nameExists:
        nameExists = True
    else:
        nameExists=False


    result = {}
    result['nameExists'] = nameExists

    return JsonResponse(result,safe=False)



def checkUniquenessOfserial_start(request):
    serial_start = request.POST['serial_start']
    id = request.POST['id']
    if id == '' or id == None:
        nameExists = category.objects.filter(serial_start=serial_start).exists()

    else:
        nameExists = category.objects.filter(serial_start=serial_start).exclude(id=id).exists()


    if nameExists:
        nameExists = True
    else:
        nameExists=False


    result = {}
    result['nameExists'] = nameExists

    return JsonResponse(result,safe=False)




def generate_part_num(categoryObject,sizeObject):
    count_of_items_of_this_category = item.objects.filter(Q(category__id=categoryObject.id)
    & Q(size__id=sizeObject.id)).order_by('-higher_count') 
    try:
        count_of_items_of_this_category = count_of_items_of_this_category[0].higher_count
    except:
        count_of_items_of_this_category = 0
        

    count_of_items_of_this_category = count_of_items_of_this_category+1


    part_num = str(f"{int(categoryObject.serial_start):04}")
    part_num = part_num + str(f"{int(sizeObject.code):02}")
    part_num = part_num + str(f"{count_of_items_of_this_category:04}")
    

    

    return [part_num,count_of_items_of_this_category]
