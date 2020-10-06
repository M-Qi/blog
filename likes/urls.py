from django.urls import path
from . import views
app_name='like'
urlpatterns = [
    path('',views.like_num,name='like_change')
]