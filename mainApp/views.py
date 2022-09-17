from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.contrib.auth.models import Group
import datetime




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

@login_required
def show_factories(request):
    context = {
        
    }
    return render (request, 'elements/show_factories.html', context)

@login_required
def show_items(request):
    context = {
        
    }
    return render (request, 'elements/show_items.html', context)




