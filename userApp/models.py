from django.contrib.auth.hashers import make_password
from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)



class CustomUserManager(BaseUserManager):
    def create_user(self, email, username,first_name,last_name,password=None,phone=None,id_number=None,address=None, **extra_fields):
        if not username:
            raise ValueError('Users must have an username')

        user = self.model(
            email=self.normalize_email(email),
            password=make_password(password),
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            id_number=id_number,
            **extra_fields
        )

        # user.set_password(password)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        user = self.model(
            username=username,
            password=make_password(password),
            **extra_fields
        )
        user.is_admin = True
        user.is_staff = True
        user.set_password(password)
        user.save(using=self._db)
        return user





class permissionGeneral(models.Model):
    name = models.CharField(max_length=500,default=None)
    nameEn = models.CharField(max_length=500,default=None,null=True)
    number = models.IntegerField(default=0)
    mainNameEn = models.CharField(max_length=500,default=None,null=True)
    mainNameAr = models.CharField(max_length=500,default=None,null=True)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)


    class Meta:
        db_table = "permissionGeneral"


    def to_json(self):
        return {
            'id' :self.id,
            'name':self.name,
            'nameEn':self.nameEn
            }
        

    def __str__(self):
        return self.name



class role(models.Model):
    permissionGeneral = models.ManyToManyField(permissionGeneral)
    name = models.CharField(max_length=500,default=None)
    name_en = models.CharField(max_length=500,default=None)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    

    class Meta:
        db_table = "role"


    def to_json(self):
        return {
            'id' :self.id,
            'name': self.name,
            'created': self.created,
            'allPermissions':[permissionOfUser.name for permissionOfUser in self.permissionGeneral.all()] ,
            'numberOfPermissions': len(self.permissionGeneral.all())
            }
        

    def __str__(self):
        return self.id



class User(AbstractBaseUser):
    username = models.CharField(max_length=100,null=True,blank=True,unique=True,)
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)

    image = models.ForeignKey('mainApp.attachmentTranscript',on_delete=models.PROTECT,null=True,blank=True)
    email = models.EmailField(verbose_name='email address',max_length=255)
    approved = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    phone = models.CharField(max_length=40,null=True,blank=True)
    address = models.TextField(default=None,null=True)
    id_number = models.TextField(default=None,null=True)
    role = models.ForeignKey(role,null=True, on_delete=models.PROTECT)
    deleted = models.DateTimeField(null=True,blank=True)
    created  = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']
    

    objects = CustomUserManager()

    def __str__(self): 
        return self.username
    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def to_json(self):
        return {
            'id':self.id,
            'username':self.username,
            'role_name':self.role.name if self.role is not None else '',
            'role_name_en':self.role.name_en if self.role is not None else '',
            'first_name':self.first_name,
            'last_name':self.last_name,
            'email':self.email,
            'id_number':self.id_number,
        }
