from django.urls import  path, re_path
from user.views import *

app_name = 'user'
urlpatterns = [
    
    path('register/', create_user, name='create_user'),
    path('is-user-exist/', check_user_name, name='user-exist'),
   
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('get-unit/', get_unit, name='get-unit'),
    # path('add-user/',add_user,name="add_user"),
    path('settings/unit/', add_unit, name='units'),
    path('load_state/', load_state, name='state'),
    
]