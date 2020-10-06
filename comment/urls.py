from django.urls import path
from . import views
app_name='commit'
urlpatterns =[
    path('update_commit/',views.update_commit,name='update_commit'),

]

