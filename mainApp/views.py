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
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.views.decorators.csrf import csrf_protect
from datetime import datetime, timedelta,date

from mainApp.models import *

@login_required
def home(request):



    context = {
        
    }
    return render (request, 'index.html', context)




@login_required
def show_companies(request):
    context = {
        
    }
    return render (request, 'elements/show_companies.html', context)

@login_required
def show_representatives(request):
    context = {
        
    }
    return render (request, 'elements/show_representatives.html', context)






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
            (Q(size__size__contains=searchKey) |
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
    all_size = size.objects.filter( Q(deleted_date=None))
    all_color = color.objects.filter( Q(deleted_date=None))
    
    context = {
        'categoryData':dataToInsert,
        'type':typeOfEntry,
        'all_factory':all_factory,
        'all_size':all_size,
        'all_color':all_color,
        }


    if request.method=='POST':
        name = request.POST['name']
        name_en = request.POST['name_en']
        year = request.POST['year']
        serial_start = request.POST['serial_start']
        colorObject = request.POST['color']
        sizeObject = request.POST['size']
        details = request.POST['details']
        factoryObject = request.POST['factory']

        try:
            factoryObject = factory.objects.get(id=factoryObject)
        except:
            factoryObject = None


        
        try:
            colorObject = color.objects.get(id=colorObject)
        except:
            colorObject = None

        
        try:
            sizeObject = size.objects.get(id=sizeObject)
        except:
            sizeObject = None

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

        print("----------------------------------")
        print(filedetails)




        if typeOfEntry == 'new':
            try:
                attachmentTranscriptObject = attachmentTranscript.objects.create(file = filedetails,content_type=filedetails.content_type,name=filedetails.name,table_name="category")
                attachmentTranscriptObject.save()
            except:
                attachmentTranscriptObject = None

            categorynew = category.objects.create(name=name,name_en=name_en,details=details,serial_start=serial_start,year=year, factory=factoryObject,size=sizeObject,color=colorObject,  created_by=request.user,image=attachmentTranscriptObject)
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
            dataToInsert.update(name=name,name_en=name_en,details=details,serial_start=serial_start,year=year, factory=factoryObject,size=sizeObject,color=colorObject,  updated_by=request.user,updated_date=datetime.now(),image=attachmentTranscriptObject)
            

 
        urlLink = reverse("mainApp:listOf_category")
        return redirect(urlLink)
    elif request.method=='GET':
        return render(request,'category/addnew.html',context)
    


@login_required
def delete_category(request):
    categoryId = request.POST['id']


    categoryDetails=category.objects.filter(Q(id=categoryId) & Q(deleted=None))
    categoryDetails.update(deleted_date = datetime.now())



   
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


    factoryDetails=factory.objects.filter(Q(id=factoryId) & Q(deleted=None))
    factoryDetails.update(deleted_date = datetime.now())



   
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


    sectorDetails=sector.objects.filter(Q(id=sectorId) & Q(deleted=None))
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


    companyDetails=company.objects.filter(Q(id=companyId) & Q(deleted=None))
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




