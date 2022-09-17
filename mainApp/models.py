from datetime import datetime
from django.conf import settings
from django.db import models
from userApp.models import User
from django.core.validators import int_list_validator
from uuid import uuid4
import os

from django.db.models.query_utils import select_related_descend
from django.db.models import Q,Avg
# Create your models here.





def path_and_renameListing(instance, filename):
    try:
        tableName = instance.table_name
        upload_to = 'docs/' + tableName
    except:
        upload_to = 'docs/'

    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class attachmentTranscript(models.Model):
    file = models.FileField('ListDoc', upload_to=path_and_renameListing)
    postDate = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    content_type = models.CharField(max_length=500,null=True,default=None)
    name = models.TextField(default=None)
    table_name = models.CharField(max_length=150,null=True,blank=True)
    
    
    @property
    def filename(self):
        name = self.file.name.split("/")[1].replace('_',' ').replace('-',' ')
        return name

    
    class Meta:
        db_table = "attachmenttranscript"



#المصانع
class factory(models.Model):
    name = models.CharField(max_length=500,default=None)
    name_en = models.CharField(max_length=500,default=None)
    head_phone = models.CharField(max_length=500,default=None)
    factory_phone = models.CharField(max_length=500,default=None)
    tax_number = models.CharField(max_length=500,default=None)
    address = models.TextField(default=None,null=True)
    image = models.ForeignKey(attachmentTranscript,on_delete=models.PROTECT,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    # ///////// new updates
    created_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True)
    updated_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name= "user_factory_updated")    
    deleted_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name="user_factory_delete")    
    updated_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    deleted_date = models.DateTimeField(null=True,blank=True)



    class Meta:
        db_table = "factory"


    def to_json(self):
        return {
            'id' :self.id,
            'name' :self.name,
            'name_en' :self.name_en,
            'created':self.created
            }

    def __str__(self):
        return self.name

#الشركات
class company(models.Model):
    name = models.CharField(max_length=500,default=None)
    name_en = models.CharField(max_length=500,default=None)
    head_phone = models.CharField(max_length=500,default=None)
    company_phone = models.CharField(max_length=500,default=None)
    tax_number = models.CharField(max_length=500,default=None)
    address = models.TextField(default=None,null=True)
    image = models.ForeignKey(attachmentTranscript,on_delete=models.PROTECT,null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)

    # ///////// new updates
    created_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True)
    updated_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name= "user_company_updated")    
    deleted_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name="user_company_delete")    
    updated_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    deleted_date = models.DateTimeField(null=True,blank=True)



    class Meta:
        db_table = "company"


    def to_json(self):
        return {
            'id' :self.id,
            'name' :self.name,
            'name_en' :self.name_en,
            'created':self.created
            }

    def __str__(self):
        return self.name
