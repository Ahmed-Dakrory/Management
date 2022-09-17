from django.utils import translation
from django.views.generic.base import View
import json

from datetime import datetime
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.conf import settings  # this is a good example of extra
                                  # context you might need across templates
from django.http import JsonResponse
from django.db.models import Q
def defaultContextProcessor(request):
    # you can declare any variable that you would like and pass 
    # them as a dictionary to be added to each template's context:
    

    try:
        language = request.session['language']
    except:
        request.session['language'] = 'ar'
        language = 'ar'

    translation.activate(language)
    user =request.user
    if user.is_authenticated:
        userProfile = user
    else:
        userProfile = None
    
    
    if language =='ar':
        checked = True
    elif language == 'en':
        checked = False
    else:
        checked = True

    return dict(
        checked=checked,
        userProfile = userProfile,
        current_date = datetime.now()    
    )


def check_language(request):
    # if Language.objects.filter(id=1).exists:
    #     lng = Language.objects.first().lan
    lng = request.session['language']
    print(lng,"lan")
    if lng =='ar':
        return {'checked':True}
    elif lng == 'en':
        return {'checked':False}
    else:
        return {'checked':True}

