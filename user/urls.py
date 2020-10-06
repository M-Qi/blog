
from django.urls import path,include
from . import views as v
app_name='user'
urlpatterns = [

    path('login/',v.login,name='login'),
    path('login_modal/',v.login_modal,name='login_modal'),
    path('reg/',v.register,name='register'),
    path('user_info/',v.user_info,name='info'),
    path('logout/',v.logout,name='logout'),
    path('change_nickname/',v.change_nickname,name='change_nickname'),
    path('change_password/',v.change_password,name='change_password'),
    path('bind_email/',v.bind_email,name='bind_email'),
    path('send_email/',v.send_email,name='send_email'),
    path('forget_password/',v.forget_password,name='forget_password'),
]
