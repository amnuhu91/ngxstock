from django.contrib import admin
#from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm
from user.models import *
from user.forms import *
# Register your models here.

# class UserAdmin(BaseUserAdmin):
#   form = CustomUserCreationForm
#   fieldsets = (
#       (None, {'fields': ('username', 'password', )}),
#       (_('Personal info'), {'fields': ('first_name', 'last_name',)}),
#       (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
#                                      'groups', 'user_permissions')}),
#       (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
#         (_('user_info'), {'fields': ( )}),
#   )
#   add_fieldsets = (
#       (None, {
#           'classes': ('wide', ),
#           'fields': ('username', 'password1', 'password2','first_name','last_name','phone_number','cadre','ipps_no','salary_scale','grade','step'),
#       }),
#   )


class userAdmin(UserAdmin):
    list_display=['id','ipps_no','username','user_type','first_name','last_name']
    list_filter=['ipps_no','user_name','user_type']
    list_editable=['user_type','first_name','last_name']

admin.site.register(Local_Government)
admin.site.register(State)
admin.site.register(Unit)
admin.site.register(Department)
admin.site.register(User,UserAdmin)
# admin.site.register(Contact)
# admin.site.register(Residence)
# admin.site.register(Member, memberAdmin)
admin.site.register(Employment)
# admin.site.register(NextOfKing)
admin.site.register(Welcome)
admin.site.register(FreQuestion)
admin.site.register(Management)
admin.site.register(Supervisor)
