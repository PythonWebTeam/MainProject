from django.db import connection
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from account.models import *


class UserInfoManageView(View):
    def get(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        username = request.session.get("username")
        user = User.objects.filter(username=username)[0]
        order_list = Order.objects.filter(user_id=user.id)
        return render(request, "user_info_manage.html", {"user": user, "order_list": order_list})

    def post(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        data = request.POST
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        username = request.session.get("username")
        user = User.objects.filter(username=username)[0]
        order_list = Order.objects.filter(user_id=user.id)
        new_username = data.get("username")  #
        email = data.get("email")  #
        phone = data.get("phone")  #
        prov = data.get("prov")
        city = data.get("city")
        county = data.get("county")
        addr = data.get("addr")
        if User.objects.filter(username=new_username):
            msg = "该用户名已存在"
            return render(request, "user_info_manage.html", {"user": user, "order_list": order_list, "msg": msg})
        else:
            user.username = new_username
            user.email = email
            user.phone = phone
            user.prov = prov
            user.city = city
            user.county = county
            user.details = addr
            return render(request, "user_info_manage.html", {"user": user, "order_list": order_list})


class ChangePasswordView(View):
    def post(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        username = request.session.get("username")
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        user = User.objects.filter(username=username)[0]
        order_list = Order.objects.filter(user_id=user.id)

        if user.password != old_password:
            return render(request, "user_info_manage.html",
                          {"user": user, "order_list": order_list, "return_msg": "原密码错误"})
        else:
            user.password = new_password
            user.save()
            return render(request, "user_info_manage.html",
                          {"user": user, "order_list": order_list, "return_msg": "修改成功"})


def order_info_manage_view(request):
    return render(request, "order_info_manage.html")


class ShopCartView(View):
    def get(self, request):
        service_id=
        return render(request, "shop_cart.html")


def vendor_info_manage_view(request):
    return render(request, "vendor_info_manage.html")


def shop_info_manage_view(request):
    return render(request, "shop_info_manage.html")


def product_manage_view(request):
    return render(request, "product_manage.html")


def order_manage_view(request):
    return render(request, "order_manage.html")


def service_manage_view(request):
    return render(request, "service_manage.html")


def business_data_view(request):
    return render(request, "business_data.html")


class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect("/")
