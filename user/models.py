from django.db import models
#from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser, Group
from random import randint
from datetime import datetime
from django.utils.timezone import  now
from django.core.mail import send_mail
from django.core.validators import MinValueValidator, MaxValueValidator
# Create your models here.

class State(models.Model):
    state_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.state_name}"


class Local_Government(models.Model):
    lga_name = models.CharField(max_length=50)
    state_name = models.ForeignKey(State, on_delete=models.CASCADE, default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return  self.lga_name




class Department(models.Model):
    depart_name = models.CharField(max_length=200)
    created_by = models.ForeignKey('User', on_delete=models.DO_NOTHING,default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.depart_name
class Unit(models.Model):
    unit_name = models.CharField(max_length=100, blank=True, null=True)
    depart_name = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True)
    created_by = models.ForeignKey('User', on_delete=models.DO_NOTHING,default=1,related_name="unit")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.unit_name

# class NextOfKing(models.Model):
#     user = models.ForeignKey('User',on_delete=models.SET_NULL, null=True)
#     user_photo = models.ImageField(upload_to='user/nextofking',null=False, blank=False)
#     next_of_king_name= models.CharField(max_length=200)
#     next_of_king_addr = models.TextField(verbose_name='Next of king Address')
#     next_of_king_phone_number = models.PositiveBigIntegerField()
#     relation = models.CharField(max_length=40)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self) -> str:
#         return f"{ self.user} next of king {self.next_of_king_name}"
    
# class Contact(models.Model):
#     user = models.ForeignKey('User',on_delete=models.SET_NULL, null=True)
#     contact_addr = models.CharField(max_length=200, verbose_name='Contact Address',)
#     state = models.ForeignKey(State, on_delete=models.PROTECT)
#     lga = models.ForeignKey(Local_Government, on_delete=models.PROTECT)
#     zip_code = models.PositiveBigIntegerField(null=True,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self) -> str:
#         return f"{self.user} {self.contact_addr} state:{self.state} and LGA: {self.lga}"
# class Residence(models.Model):
#     user = models.ForeignKey('User',on_delete=models.SET_NULL, null=True)
#     residense_addr = models.CharField(max_length=200, verbose_name='Residence Address',)
#     state_of_residence = models.ForeignKey(State, on_delete=models.PROTECT)
#     lga_of_residence = models.ForeignKey(Local_Government, on_delete=models.PROTECT)
#     zip_code = models.PositiveIntegerField(null=True,blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self) -> str:
#         return f"{self.user} {self.residense_addr} state:{self.state_of_residence} and LGA: {self.lga_of_residence}"
# class Member(models.Model):
#     first_name = models.CharField(max_length=100)
#     last_name = models.CharField(max_length=100)
#     file_number = models.PositiveIntegerField()
#     ippis_no = models.PositiveIntegerField()
#     phone_number = models.CharField(max_length=20)
#     is_staff=models.BooleanField(default=False)
#     is_active=models.BooleanField(default=True)
#     added_by= models.ForeignKey('User', on_delete=models.DO_NOTHING,default=1)
#     created_at = models.DateTimeField(auto_now=True)
    
#     def __str__(self):
#         return str(self.file_number)


class User(AbstractUser) :
    user_type= models.CharField(max_length=30,choices=(('procurement','procurement'),('department','department'),('supplier','supplier')),default='department')
    middle_name = models.CharField(max_length=150,blank=True,null=True)
    depart =models.ForeignKey(Department, on_delete=models.PROTECT, null=True, blank=True,verbose_name="Department")
    user_unit =models.ForeignKey(Unit, on_delete=models.PROTECT,  null=True, blank=True,verbose_name="Unit")
    phone_number = models.CharField(max_length=14, default="+23480")
    email = models.EmailField(max_length=100, null=True, blank=True)
    rank=models.CharField(max_length=30,default="Procurement officer I")
    created_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        # if  self.member_id ==None:
        return str(self.username)
        # return str(self.member_id.id)
        
class Employment(models.Model):
    class salary_scale_choice(models.TextChoices):
        CONHESS = 'CONHESS'
        CONMESS = 'CONMESS'
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    user_photo = models.ImageField(upload_to='user/profile',null=False, blank=False)
    department = models.ForeignKey(Department,on_delete=models.SET_NULL, null=True, blank=True)
    unit = models.ForeignKey(Unit,on_delete=models.SET_NULL, null=True, blank=True)
    cadre = models.CharField(max_length=100)
    salary_scale= models.CharField(max_length=30, choices= salary_scale_choice.choices)
    grade = models.PositiveIntegerField( )
    step = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.username


class FreQuestion(models.Model):
    question_title=models.CharField(max_length=200)
    answer= models.TextField(help_text="type the answer of the question")
    added_by=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.question_title
class Supervisor(models.Model):
    title=models.CharField(max_length=100)
    added_by=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title

class Management(models.Model):
    RANK=(
        
        ('President','President'),
        ('Vice','Vice President'),
        ('Secratery','Secratery'),
        ('PRO','P.R.O'),
        ('Auditor','Auditor'),
        ('Investment_super','Inves. Supervisor'),

        ('Staff','Staff')
        
    )
    SUPERVISOR=(
        
        ('President','President'),
        ('Vice','Vice President'),
        ('Secratery','Secratery'),
        ('PRO','P.R.O'),
        ('Staff','Staff')
        
    )
    
    name=models.CharField(max_length=100,help_text="Enter full name")
    rank=models.CharField(max_length=20,choices=RANK)
    supervisor=models.CharField(max_length=20,choices=SUPERVISOR,default="President")
    added_by=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def save(self,*args,**kwargs):
        if self.rank =="President":
            self.supervisor=''
        else:
            pass
        super(Management,self).save(*args,**kwargs)
    def __str__(self):
        return self.name

class Welcome(models.Model):
    message=models.CharField(max_length=200,verbose_name="Caption")
    sologan = models.CharField(max_length=150)
    text_msg= models.TextField(help_text="enter welcome message")
    created_by=models.ForeignKey(User,on_delete=models.DO_NOTHING,default=1)





    





