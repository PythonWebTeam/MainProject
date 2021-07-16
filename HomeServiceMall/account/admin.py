from django.contrib import admin

from .models import *


class UserAdmin(admin.ModelAdmin):
    search_fields = ("username",)


admin.site.register(User, UserAdmin)
admin.site.register(Cart)

admin.site.register(Type)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', "status", "sort", "sales", "shop")
    ordering = ("-sales",)
    search_fields = ('id', 'name', "shop", "sort",)


admin.site.register(Service, ServiceAdmin)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'create_time', 'user')
    search_fields = ('name',)


admin.site.register(Shop, ShopAdmin)


class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'send_time', 'send_type')


admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'create_time', 'start_time', 'end_time', 'pay_status', 'star')
    search_fields = ('service', 'user',)


admin.site.register(ApplyforShop)

admin.site.register(Order, OrderAdmin)
