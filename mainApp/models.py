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
            'factory_phone' :self.factory_phone,
            'head_phone' :self.head_phone,
            'address' :self.address,
            'tax_number' :self.tax_number,
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
            'company_phone' :self.company_phone,
            'head_phone' :self.head_phone,
            'address' :self.address,
            'tax_number' :self.tax_number,
            'created':self.created
            }

    def __str__(self):
        return self.name


#قطاع
class sector(models.Model):
    name = models.CharField(max_length=500,default=None)
    name_en = models.CharField(max_length=500,default=None)
    floor = models.CharField(max_length=500,default=None)
    image = models.ForeignKey(attachmentTranscript,on_delete=models.PROTECT,null=True,blank=True)
    
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    # ///////// new updates
    created_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True)
    updated_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name= "user_sector_updated")    
    deleted_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name="user_sector_delete")    
    updated_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    deleted_date = models.DateTimeField(null=True,blank=True)



    class Meta:
        db_table = "sector"


    def to_json(self):
        return {
            'id' :self.id,
            'name' :self.name,
            'name_en' :self.name_en,
            'floor' :self.floor,
            'created':self.created
            }

    def __str__(self):
        return self.name


class color(models.Model):
    name = models.CharField(max_length=500,default=None)
    name_en = models.CharField(max_length=500,default=None)
    code = models.CharField(max_length=500,default=None)
    
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    # ///////// new updates
    created_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True)
    updated_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name= "user_color_updated")    
    deleted_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name="user_color_delete")    
    updated_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    deleted_date = models.DateTimeField(null=True,blank=True)



    class Meta:
        db_table = "color"


    def to_json(self):
        return {
            'id' :self.id,
            'name' :self.name,
            'name_en' :self.name_en,
            'code' :self.code,
            'created':self.created
            }

    def __str__(self):
        return self.name



class size(models.Model):
    size = models.CharField(max_length=500,default=None)
    code = models.CharField(max_length=500,default=None)
    
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    # ///////// new updates
    created_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True)
    updated_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name= "user_size_updated")    
    deleted_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name="user_size_delete")    
    updated_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    deleted_date = models.DateTimeField(null=True,blank=True)



    class Meta:
        db_table = "size"


    def to_json(self):
        return {
            'id' :self.id,
            'size' :self.size,
            'code' :self.code,
            'created':self.created
            }

    def __str__(self):
        return self.name




#الفئة
class category(models.Model):
    name = models.CharField(max_length=500,default=None)
    name_en = models.CharField(max_length=500,default=None)
    details = models.TextField(default=None)
    year = models.TextField(default=None)
    color = models.ForeignKey(color,on_delete=models.PROTECT,null=True,blank=True)
    serial_start = models.TextField(default=None,unique=True)
    factory = models.ForeignKey(factory,on_delete=models.PROTECT,null=True,blank=True)
    image = models.ForeignKey(attachmentTranscript,on_delete=models.PROTECT,null=True,blank=True)
    
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    # ///////// new updates
    created_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True)
    updated_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name= "user_category_updated")    
    deleted_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name="user_category_delete")    
    updated_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    deleted_date = models.DateTimeField(null=True,blank=True)



    class Meta:
        db_table = "category"


    def to_json(self):
        return {
            'id' :self.id,
            'name' :self.name,
            'name_en' :self.name_en,
            'year' :self.year,
            'color_name' :self.color.name if self.color is not None else '',
            'color_name_en' :self.color.name_en if self.color is not None else '',
            'factory_name' :self.factory.name if self.factory is not None else '',
            'factory_name_en' :self.factory.name_en if self.factory is not None else '',
            'serial_start' :self.serial_start,
            'details' :self.details,
            'image' :self.image.file.url if self.image is not None else '',
            'created':self.created
            }

    def __str__(self):
        return self.name



#البند
class item(models.Model):
    part_num = models.CharField(max_length=500,default=None)
    details = models.TextField(default=None)
    exists = models.BooleanField(default=True)
    is_returned = models.BooleanField(default=True)
    higher_count = models.IntegerField(default=True)
    size = models.ForeignKey(size,on_delete=models.PROTECT,null=True,blank=True)
    company_with = models.ForeignKey(company,on_delete=models.PROTECT,null=True,blank=True)
    representitive_with = models.ForeignKey(User,on_delete=models.PROTECT,null=True,blank=True,related_name= "user_item_representitive")
    category = models.ForeignKey(category,on_delete=models.PROTECT,null=True,blank=True)
    last_out_date = models.DateTimeField(null=True,blank=True)
    last_return_date = models.DateTimeField(null=True,blank=True)
    
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
    # ///////// new updates
    created_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True)
    updated_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name= "user_item_updated")    
    deleted_by = models.ForeignKey('userApp.User',on_delete=models.PROTECT,null=True,blank=True,related_name="user_item_delete")    
    updated_date = models.DateTimeField(auto_now=True,null=True,blank=True)
    deleted_date = models.DateTimeField(null=True,blank=True)



    class Meta:
        db_table = "item"


    def to_json(self):
        return {
            'id' :self.id,
            'part_num' :self.part_num,
            'color_name' :self.category.color.name if self.category.color is not None else '',
            'color_name_en' :self.category.color.name_en if self.category.color is not None else '',
            'size' :self.size.size if self.size is not None else '',
            'size_code' :self.size.code if self.size is not None else '',
            'factory_name' :self.category.factory.name if self.category.factory is not None else '',
            'factory_name_en' :self.category.factory.name_en if self.category.factory is not None else '',
            'company_with_name' :self.company_with.name if self.company_with is not None else '',
            'company_with_name_en' :self.company_with.name_en if self.company_with is not None else '',
            'representitive_with_name' :self.representitive_with.username if self.representitive_with is not None else '',
            'representitive_with_phone' :self.representitive_with.phone if self.representitive_with is not None else '',
            'last_out_date' :self.last_out_date if self.last_out_date is not None else '',
            'last_return_date' :self.last_return_date if self.last_return_date is not None else '',
            'details' :self.details,
            'exists' :self.exists,
            'is_returned':self.is_returned,
            'image' :self.category.image.file.url if self.category.image is not None else '',
            'created':self.created
            }

    def __str__(self):
        return self.name


