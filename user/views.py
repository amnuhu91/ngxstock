from django.shortcuts import render, get_object_or_404,redirect, reverse, HttpResponseRedirect, HttpResponse
from django.core.exceptions import  ObjectDoesNotExist
from django.http import JsonResponse
from django.core.mail import send_mail
from user.forms import *
from user.models import *
from django.db import IntegrityError
from django.db.models import *

# from utils import get_loans, make_payment_transaction
import requests as rq
from requests.auth import HTTPBasicAuth



import calendar
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
from openpyxl import *
#modeules



def home(request):
    context={}
    welcome= Welcome.objects.order_by('-id').first()
    
    context['welcome']=welcome
    return render(request,'user/index.html',context)

def freq_question(request):
    context={}
    freq_question= FreQuestion.objects.all().order_by('-id')
    context['freq']= freq_question
    return render(request,'user/freq.html',context)


def management(request):
    context={}
    managers= Management.objects.values('id','name','rank','supervisor')#.order_by('id')
   
    mans= json.dumps(list(managers))
    print('managers',mans)
    context['managers']=mans
    return render(request,'user/org.html',context)



@login_required
def add_faq(request):
    form = AddFAQForm()
    context={'form':form}
    context['faq']=True
    if request.method=="POST":
        form=AddFAQForm(request.POST)
        if form.is_valid():
            faq=form.save(commit=False)
            faq.added_by=User.objects.get(username=request.user)
            faq.save()
            
            context['msg']=f"added successfully."
            context['msg_c']="success"
    return render(request,'user/add_bank.html',context)


@csrf_exempt
#@login_required
def check_user_name(request):
    username = request.POST.get('username')
    print('USERNAME',username)
    is_user_exist =User.objects.filter(username=username).exists()
    print(is_user_exist)
    return JsonResponse(is_user_exist, safe=False)
def create_user(request):
    form=RegisterMemberForm()
    context={'form':form}
    
    form = RegisterMemberForm()
    
    if request.method=='POST':
        
        form = RegisterMemberForm(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            middle_name = form.cleaned_data['middle_name']
            department_id = form.cleaned_data['depart']
            unit_id = form.cleaned_data['user_unit']
            # department=Department.objects.get(id=department_id)
            # unit=Unit.objects.get(id=unit_id)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            password2 = form.cleaned_data['password2']
            # print(f'first name:{first_name} last name: {last_name} middle name: {middle_name} department: {department} unit: {unit} password:{password} password 2:{password2}')
            if password == password2:
                try:
                    
                    user = User.objects.create_user(
                    first_name=first_name,
                    last_name =last_name,
                    middle_name = middle_name,
                    depart=department_id,
                    user_unit=unit_id,
                    username = username,
                    password = password
                )
                    user.save()
                    log_user = authenticate(request, username=username, password=password)
                    if log_user is not None:
                        login(request, log_user)
                        return redirect(reverse('procurement:send_request'))
                except IntegrityError:
                    print('USRNAME TAKEN')
                    context['msg']=f"username \'{username}\' not available. PLease choose another one."
                    context['msg_c']='danger'
                    return render(request, 'user/add_member.html', context)
            else:
                msg = 'password does not match !!!'
                context['message']=msg
                return render(request, 'user/add_member.html', context)
        else:
            return render(request, 'user/add_member.html', context)
    # else:
    #     context['msg']=f"Member with IPPIS: {} already registered."
    #     context['msg_c']='info'
    #     return render(request,'includes/messages.html',context)
    return render(request, 'user/add_member.html', context)

#get depart and Unit
# @login_required
def get_unit(request):
    dept_id = request.GET.get('dept_id')
    print('Depart id',dept_id)
    if (dept_id !='' or None):
        print('dept id', dept_id)
        units = Unit.objects.filter(depart_name=dept_id)
        #return render(request,'user/units.html',{"units":units})
        return render(request, 'user/units.html',{"units":units})
    units =[]
    return render(request,'user/units.html',{"units":units})



# @login_required
# def add_user(request):
#     form=AddUserupplyForm()
#     supplier_form=AddSupplierForm()
#     context={'form':form,'supply_form':supplier_form}
#     print('GET REQUEST')
#     if request.method=='POST':
        
#         form = AddUserupplyForm(request.POST)
#         print('Form is valid',form.is_valid())
#         print('for errors',form.errors)
#         depart = Department.objects.get(depart_name="Supplier")
#         unit=Unit.objects.get(unit_name="Supplier")
#         if form.is_valid():
#             first_name=form.cleaned_data['first_name']
#             last_name=form.cleaned_data['last_name'] or ""
#             middle_name = form.cleaned_data['middle_name']
#             department_id = form.cleaned_data['depart'] or depart
#             unit_id = form.cleaned_data['user_unit'] or unit
#             user_type=form.cleaned_data['user_type']
#             username = form.cleaned_data['username']
#             password = form.cleaned_data['password']
#             password2 = form.cleaned_data['password2']

            
#             print('USER TYPE',user_type)
#             print(f'first name:{first_name} last name: {last_name} middle name: {middle_name} department: {department_id} user type:{user_type} unit: {unit_id} password:{password} password 2:{password2}')
#             if password == password2:
                
#                 try:
                    
#                    if user_type =="supplier": 
#                         supplier_name=request.POST.get('supplier_name')
#                         supplier_address=request.POST.get('address')
#                         supplier_phone=request.POST.get('phone_number')
#                         supplier_email=request.POST.get('email')
#                         user = User.objects.create_user(
#                         first_name=first_name,
#                         last_name =last_name,
#                         middle_name = middle_name,
#                         depart=department_id,
#                         user_unit=unit_id,
#                         username = username,
#                         user_type=user_type,
#                         password = password
#                     )
#                         user.save()
#                         supplier=Supplier.objects.create(
#                             supplier_name=supplier_name,
#                             added_by=User.objects.filter(username=request.user).first(),
#                             user=User.objects.get(username=user.username),
#                             address= supplier_address,
#                             phone_number=supplier_phone,
#                             email=supplier_email

#                         )
#                    else:
#                        rank=request.POST.get('rank') or "department"
#                        user = User.objects.create_user(
#                         first_name=first_name,
#                         last_name =last_name,
#                         middle_name = middle_name,
#                         rank=rank,
#                         depart=department_id,
#                         user_unit=unit_id,
#                         username = username,
#                         user_type=user_type,
#                         password = password
#                     )
                   
#                    log_user = authenticate(request, username=username, password=password)
#                    if log_user is not None:
#                         login(request, log_user)
#                         print('USER TYPE',user.user_type)
#                         if user.user_type== "procurement" :
#                             return redirect(reverse('procurement:request_list'))
#                         elif user.user_type=="supplier":
#                             return redirect(reverse('procurement:submit_quotation'))
#                         else: return redirect(reverse('procurement:send_request'))
                   
#                 except IntegrityError:
#                     print('USRNAME TAKEN')
#                     context['msg']=f"username \'{username}\' not available. PLease choose another one."
#                     context['msg_c']='danger'
#                     return render(request, 'user/add_user.html', context)
#             else:
#                 msg = 'password does not match !!!'
#                 context['message']=msg
#                 return render(request, 'user/add_user.html', context)
#     return render(request,'user/add_user.html',context)



#short login
def login_user(request):
    # user=User.objects.get(username=request.user)
    print('User',request.user)
    if request.method == 'POST':
        username =request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        print('user type',user.user_type)
        if user is not None:
            login(request, user)
            next = request.POST.get('next')
            if next !='' and next is not None:
                #print(next)
                return redirect(next)
            if user.user_type== "procurement" :
                return redirect(reverse('procurement:request_list'))
            elif user.user_type=="supplier":
                return redirect(reverse('procurement:submit_quotation'))
            else: return redirect(reverse('procurement:send_request'))
                
            # return redirect(reverse('procurement:send_request'))
        context={
            'msg':"invalid username or password",
            'msg_c':'danger'
        }
        return render(request,'user/login.html',context)
            
        
    return render(request,'user/login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect(reverse('home'))







@login_required
def add_unit(request):
    form = AddUnitForm()
    context={'form':form}
    if request.method=="POST":
        form = AddUnitForm(request.POST)
        if form.is_valid():
            u= form.save(commit=False)
            u.created_by= request.user
            u.save()
            context['msg']=f"{u.unit_name} was added successfully to {u.depart_name.depart_name}."
            context['msg_c']='success'
            return render(request,'user/department_form.html',context) 

    return render(request,'user/department_form.html',context)

@login_required
def load_state(request):
    state_id = request.GET.get('state_id')
    lgas =Local_Government.objects.filter(state_name=state_id)
    print(lgas)
    return render(request,'user/state_list.html',{"lgas":lgas})
