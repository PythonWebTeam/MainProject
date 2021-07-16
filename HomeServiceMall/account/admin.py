from django.contrib import admin

from .models import *

admin.site.register(User)

admin.site.register(Cart)

admin.site.register(Type)


class ServiceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'price', "status", "sort", "sales", "shop")
    ordering = ("-sales",)


admin.site.register(Service, ServiceAdmin)


class ShopAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'create_time', 'user')


admin.site.register(Shop, ShopAdmin)


class EmailVerifyRecordAdmin(admin.ModelAdmin):
    list_display = ('email', 'code', 'send_time', 'send_type')


admin.site.register(EmailVerifyRecord, EmailVerifyRecordAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('service', 'user', 'create_time', 'start_time', 'end_time', 'pay_status', 'star')


admin.site.register(ApplyforShop)

admin.site.register(Order, OrderAdmin)
