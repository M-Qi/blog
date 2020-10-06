
from django.urls import path,include

from . import views
#http://127.0.0.1/blog
#http://127.0.0.1/blog/1

#http://127.0.0.1:8000
app_name='blog'
urlpatterns = [
    path('',views.blog_list,name='blog_list'),
    path('detail/<int:blog_id>/',views.blog_detail,name='detail'),
    path('type/<int:blog_type>/',views.blog_type,name='blog_type'),
    path('date/<int:year>/<int:month>/',views.blog_date,name='blog_date'),
]
