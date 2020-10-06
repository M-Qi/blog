from django.contrib import admin
from .models import Read_number,ReadDetailDate
# Register your models here.
@admin.register(Read_number)
class read_num(admin.ModelAdmin):
    list_display = ('read_num','content_object')

@admin.register(ReadDetailDate)
class ReadDetailDate(admin.ModelAdmin):
    list_display = ('date','read_num','content_object')

