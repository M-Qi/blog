from django.contrib import admin
from .models import BlogType,Blog
# Register your models here.
# 以列表的方式显示多的一端
class BlogStackedInline(admin.TabularInline):
    #关联子对象  多端
    model = Blog
    extra = 1  #可以额外编辑1个子对象




#自定义模型管理类
@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    # 显示哪几个字段
    list_display = ('id','type_name','type','parent')  #type在模型中自定义的方法
    #后台管理显示几条数据
    list_per_page = 5
    # 显示下面的下拉框
    actions_on_bottom = True
    #隐藏上面的下拉框
    actions_on_top = False
    #搜索框按照哪个字段进行搜索
    search_fields = ['type_name']
    # fields = ['']
    #内嵌方式
    inlines = [BlogStackedInline]

# 通过装饰器注册模型类
@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    #显示哪几个字段
    list_display = ('title','blog_type','author','readnumber','create_time','update_time')
    #过滤框
    list_filter = ['title','blog_type']
    #搜索框
    search_fields = ['title']

# 编辑页  编辑顺序
#     fields = ['blog_type','title','author','content']
# class UserAdmin()
    fieldsets = (
        ('基本',{'fields':['title','content']}),
        ('高级',{'fields':['blog_type','author']})
    )

"""
@admin.register(Read_number)
class Read_numberAdmin(admin.ModelAdmin):
    list_display = ('read_num','blog')

"""