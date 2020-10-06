from django.contrib import admin
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



# 纵向的展示/添加数据
class ProfileInline(admin.StackedInline):
    model = Profile # 关联的模型
    can_delete = False # 不允许删除


class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline,) # 在添加的时候展示
    list_display = ('username','nickname','email','is_staff','is_active','is_superuser')
    # 在首页增加一个nickname列
    def nickname(self,obj):
        return obj.profile.nickname
    nickname.short_description = '昵称'
# 先移除原有注册的User
admin.site.unregister(User)
# 在把刚刚重写的注册
admin.site.register(User,UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user','nickname')
