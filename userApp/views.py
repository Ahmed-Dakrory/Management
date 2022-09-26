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
from userApp.models import *

from .forms import *

# @unauthenticated_user
def user_login(request):
    
    if request.method=='POST':
        loginform=userLogin(request.POST)

        if loginform.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            print(username)
            print(password)
            user=authenticate(username=username,password=password)
            print(user)
            if user is not None: 
                # print("Exists")
                login(request,user)
                links = request.META['HTTP_REFERER'].split('next=')
                # print( links[1] )
                try:
                    return redirect(links[1])
                except:
                    return redirect("/")
        return render(request,"login.html",{'form':loginform,'flag':True})

    else:
        loginform=userLogin()
        return render(request,"login.html",{'form':loginform})


def user_logout(request):
    logout(request)
    return redirect("userApp:login")


####################  role  #################3
@login_required
def listOf_role(request):
    
    return render(request,'role/list.html',None)


@login_required
def getListOf_role(request):
    pageLength = int(request.GET['length'])
    pageNumber = int(request.GET['start'])
    draw = int(request.GET['draw'])
    searchKey = request.GET['search[value]']
    pageNumber = int(pageNumber/pageLength + 1)
    
    try:
        if searchKey == '':
            allElements = role.objects.filter( Q(id__isnull=False))
        else:
            allElements = role.objects.annotate(permissionGeneralCount=Count('permissionGeneral')).filter(Q(deleted=False) & 
            (Q(name__contains=searchKey) | Q(name_en__contains=searchKey) | Q(permissionGeneralCount__contains=searchKey)|
             Q(id__contains=searchKey) ))


        if pageLength == -1:
            if allElements !=None:
                pageLength = len(allElements)

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
def addnew_role(request):
    typeOfEntry = request.GET['type']
    if typeOfEntry == 'new':
        allSelectedPermissions = None
        dataToInsert = None
    elif typeOfEntry == 'edit':
        idOfelement = request.GET['id']
        dataToInsert = role.objects.get(id=idOfelement)
        allselectedData=dataToInsert.permissionGeneral.all()
        allSelectedPermissions=[]
        for data in allselectedData:
            allSelectedPermissions.append(data.id)

             

    
    query = permissionGeneral.objects.values('number','mainNameAr','mainNameEn').annotate(mainNumber=Count('number')).filter(id__isnull=False)
    
    all_permissionGeneral = []
    for itemPermission in query:
        itemNew = {
                    'number':itemPermission['number'],
                    'mainNameAr':itemPermission['mainNameAr'],
                    'mainNameEn':itemPermission['mainNameEn'],
                    'allPermissionsRelated':[]
                }
        allPermissionForMain = permissionGeneral.objects.filter(Q(number=itemPermission['number']))
        for itemSmallPermission in allPermissionForMain:
            itemNew['allPermissionsRelated'].append(itemSmallPermission.to_json())


        all_permissionGeneral.append(itemNew)

        
    
    context = {
        'thisElementData':dataToInsert,
        'all_permissionGeneral':all_permissionGeneral,
        'allSelectedPermissions':allSelectedPermissions
        }
    if request.method=='POST':
        # print(request.POST)
        numberOfPermission = len(all_permissionGeneral)
        nameData = request.POST['name']
        name_enData = request.POST['name_en']
       


        permissionGeneralCheckBox = request.POST.getlist('permissionGeneralCheckBox')

        
        if typeOfEntry == 'new':
            dataToInsert = role.objects.create(name=nameData,name_en=name_enData)
            dataToInsert.save()
            for item in permissionGeneralCheckBox:
                subObject = permissionGeneral.objects.get(id=item)
                dataToInsert.permissionGeneral.add(subObject)
        elif typeOfEntry == 'edit':
            # role_parts.objects.filter(id=idOfelement).update(name=nameData,role=role_Data)

            dataToInsert.permissionGeneral.clear()
            for item in permissionGeneralCheckBox:
                subObject = permissionGeneral.objects.get(Q(id=str(item)))
                dataToInsert.permissionGeneral.add(subObject)
            
            dataToInsert = role.objects.filter(id=idOfelement)
            dataToInsert.update(name = nameData)


        urlLink = reverse("userApp:listOf_role")
        return redirect(urlLink)
    elif request.method=='GET':
        return render(request,'role/addnew.html',context)
    



####################  User  #################3
@login_required
def listOf_user(request):
    
    return render(request,'user/list.html',None)


@login_required
def getListOf_user(request):
    pageLength = int(request.GET['length'])
    pageNumber = int(request.GET['start'])
    draw = int(request.GET['draw'])
    searchKey = request.GET['search[value]']
    pageNumber = int(pageNumber/pageLength + 1)
    
    try:
        if searchKey == '':
            allElements = User.objects.filter( Q(deleted=None))
        else:
            allElements = User.objects.filter(Q(deleted=None) & 
            (Q(username__contains=searchKey) |
             Q(role__name__contains=searchKey)|
             Q(role__name_en__contains=searchKey)|
             Q(email__contains=searchKey)|
             Q(id_number__contains=searchKey)|
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
def addnew_user(request):
    all_role = role.objects.all()
    typeOfEntry = request.GET['type']
    if typeOfEntry == 'new':
        dataToInsert = None
    elif typeOfEntry == 'edit':
        idOfelement = request.GET['id']
        dataToInsert = User.objects.get(id=idOfelement)
    
    
    context = {
        'all_role':all_role,
        'UserData':dataToInsert,
        'type':typeOfEntry}

    if request.method=='POST':
        emailData = request.POST['email']
        passwordData = request.POST['password']
        addressData = request.POST['address']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        phoneData = request.POST['phone']
        role_Id = request.POST['role']
        id_number = request.POST['id_number']
        

      

      
        


 

        if role_Id !='':
            role_Data = role.objects.get(id=role_Id)
        else:
            role_Data = None

        if typeOfEntry == 'new':
            usernameData = request.POST['username']
            usernew = User.objects.create_user(username=usernameData,last_name=last_name,first_name=first_name, approved=True,is_staff=True,is_active=True,  password=passwordData,email=emailData,address=addressData,phone=phoneData,role=role_Data,id_number=id_number)
            usernew.save()

            
        elif typeOfEntry == 'edit':
            dataToInsert = User.objects.filter(id=idOfelement)
            userData = User.objects.get(pk = idOfelement)
            if passwordData!='':
                userData.set_password(passwordData)
                userData.save()
            
            User.objects.filter(id=userData.id).update(email=emailData)
            dataToInsert.update(address=addressData,last_name=last_name,first_name=first_name, approved=True,is_staff=True,is_active=True, id_number=id_number,phone=phoneData,role=role_Data)
            

 
        urlLink = reverse("userApp:listOf_user")
        return redirect(urlLink)
    elif request.method=='GET':
        return render(request,'user/addnew.html',context)
    


@login_required
def delete_user(request):
    UserId = request.POST['id']


    UserDetails=User.objects.filter(Q(id=UserId) & Q(deleted=None))
    UserDetails.update(deleted = datetime.now())

    UserOfUser = User.objects.get(id = UserId)
    UserOfUser.is_active = False
    UserOfUser.save()


   
    allJson = {"Result": "Fail"}
    
    allJson['Result'] = "Success"


    if allJson != None:
        return JsonResponse(allJson, safe=False)
    else:
        allJson['Result'] = "Fail"
        return JsonResponse(allJson, safe=False)
    






def checkUniquenessOfUsername(request):
    username = request.POST['username']
    id = request.POST['id']
    if id == '' or id == None:
        nameExists = User.objects.filter(username=username).exists()

    else:
        nameExists = User.objects.filter(username=username).exclude(id=id).exists()


    if nameExists:
        nameExists = True
    else:
        nameExists=False


    result = {}
    result['nameExists'] = nameExists

    return JsonResponse(result,safe=False)


