from django import forms
from django.db import models
from user.models import *



# class CheckUserForm(forms.ModelForm):
#     class Meta:
#         model= Member
#         fields = ['file_number','ippis_no']
class RegisterMemberForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['first_name','last_name','middle_name','depart','user_unit','username','password']
    password2 = forms.CharField(required=True, label='Comfirm Password',widget=forms.TextInput(attrs={
         'autocomplete':'off',
         'type':'password'
     }))
    

    def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['user_unit'].queryset=Unit.objects.none()
            if 'depart' in self.data:
                try:
                    dept_id = int(self.data.get('depart'))
                    self.fields['user_unit'].queryset =Unit.objects.filter(depart_name=dept_id).order_by('unit_name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['unit_name'].queryset= self.instance.department.unit_set.order_by('unit_name')
    
    
    # first_name = forms.CharField(max_length=100,min_length=3, required=False)
    # last_name = forms.CharField(max_length=100,min_length=3, required=False)
    # middle_name = forms.CharField(max_length=100,min_length=3, required=False)
    # department = forms.CharField(max_length=100,min_length=3, required=False)
    # unit = forms.CharField(max_length=100,min_length=3, required=False)
    # username = forms.CharField(max_length=100,min_length=4, widget=forms.TextInput(attrs={
    #     'autocomplete':'off'
    # }))
    # email = forms.EmailField(required=False)
    # password = forms.CharField(widget=forms.PasswordInput, required=True)
    # password2 = forms.CharField(widget=forms.PasswordInput, required=True, label='Comfirm Password')

class AddUserupplyForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=User
        fields=['user_type','first_name','last_name','middle_name','depart','user_unit','username','password']
    password2 = forms.CharField(required=True, label='Comfirm Password',widget=forms.TextInput(attrs={
        'autocomplete':'off',
        'type':'password'
    }))
    

    def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['user_unit'].queryset=Unit.objects.none()
            if 'depart' in self.data:
                try:
                    dept_id = int(self.data.get('depart'))
                    self.fields['user_unit'].queryset =Unit.objects.filter(depart_name=dept_id).order_by('unit_name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['unit_name'].queryset= self.instance.department.unit_set.order_by('unit_name')
    

class EmploymentForm(forms.ModelForm):
    class Meta:
        model=Employment
        exclude =('user','created_at','updated_at')
    

    def __init__(self,*args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['unit'].queryset=Unit.objects.none()
            if 'department' in self.data:
                try:
                    dept_id = int(self.data.get('department'))
                    self.fields['unit'].queryset =Unit.objects.filter(depart_name=dept_id).order_by('unit_name')
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk:
                self.fields['unit_name'].queryset= self.instance.department.unit_set.order_by('unit_name')
    

# class ContactForm(forms.ModelForm):
    
#     class Meta:
#         model = Contact
#         exclude =('user',)
    
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         self.fields['lga'].queryset=Local_Government.objects.none()

#         if 'state' in self.data:
#             try:
#                 state_id = int(self.data.get('state'))
#                 self.fields['lga'].queryset =Local_Government.objects.filter(state_name=state_id).order_by('lga_name')
#             except (ValueError, TypeError):
#                 pass
#         elif self.instance.pk:
#             self.fields['lga'].queryset= self.instance.state.lga_name_set.order_by('lga_name')

# class ResidenceForm(forms.ModelForm):
    
#     class Meta:
#         model = Residence
#         exclude =('user',)
    
#     def __init__(self,*args,**kwargs):
#         super().__init__(*args,**kwargs)
#         self.fields['lga_of_residence'].queryset=Local_Government.objects.none()
#         print('form data',self.data)
#         if 'state_of_residence' in self.data:
#             try:
#                 state_id = int(self.data.get('state_of_residence'))
#                 self.fields['lga_of_residence'].queryset =Local_Government.objects.filter(state_name=state_id).order_by('lga_name')
#             except (ValueError, TypeError):
#                 pass
#                 #print(ValueError)
#         elif self.instance.pk:
#             self.fields['lga_of_residence'].queryset= self.instance.state_of_residence.lga_of_residence_set.order_by('lga_name')
         

# class NextofKingForm(forms.ModelForm):
    
#     class Meta:
#         model = NextOfKing
#         exclude =('user',)
         


class AddDepartmentForm(forms.ModelForm):
    class Meta:
        model=Department
        fields=['depart_name']
    
class AddUnitForm(forms.ModelForm):
    class Meta:
        model=Unit
        fields=['unit_name','depart_name']

# class AddMemberForm(forms.ModelForm):
#     class Meta:
#         model=Member
#         exclude=['added_by','created_at','is_active']
#         #fields='__all__'



class AddManagerForm(forms.ModelForm):
    class Meta:
        model=Management
        exclude=('added_by','created_at','updated_at',)
class WelcomeForm(forms.ModelForm):
    class Meta:
        model=Welcome
        fields=('message','sologan','text_msg',)

class AddFAQForm(forms.ModelForm):
    class Meta:
        model=FreQuestion
        fields=('question_title','answer',)