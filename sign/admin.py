from django.contrib import admin
from sign.models import Event, Guest


# Register your models here.
#这个是后台管理员的页面


class Eventadmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'status', 'address', 'start_time']
    search_fields = ['name'] #搜索栏
    list_filter = ['status'] #过滤器


class GuestAdmin(admin.ModelAdmin):
    list_display = ['realname', 'phone', 'email', 'sign', 'create_time', 'event']
    search_fields = ['realname', 'phone']#搜索栏
    list_filter = ['sign']#过滤器


admin.site.register(Event, Eventadmin)#将Eventadmin模块注册在Event下
admin.site.register(Guest, GuestAdmin)#将GuestAdmin模块注册在Guest下
