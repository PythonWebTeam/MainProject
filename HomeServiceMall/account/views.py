from django.contrib.auth import authenticate
from django.db import connection
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views import View

from account.models import *
from utils.util import Util


class UserInfoManageView(View):
    def get(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        username, services_sort, is_login = Util.get_basic_info(request)
        username = request.session.get("username")
        user = User.objects.filter(username=username)[0]
        if user.is_vendor:
            return redirect("/account/vendors/vendor_info_manage")
        order_list = Order.objects.filter(user_id=user.id)
        return render(request, "user_info_manage.html", {"user": user, "order_list": order_list,"username":username,"services_sort":services_sort,"is_login":is_login})

    def post(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        data = request.POST
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        username, services_sort, is_login = Util.get_basic_info(request)
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
            return render(request, "user_info_manage.html", {"user": user, "order_list": order_list, "msg": msg,"username":username,"services_sort":services_sort,"is_login":is_login})
        else:
            user.username = new_username
            user.email = email
            user.phone = phone
            user.prov = prov
            user.city = city
            user.county = county
            user.details = addr
            return render(request, "user_info_manage.html", {"user": user, "order_list": order_list,"username":username,"services_sort":services_sort,"is_login":is_login})


class ChangePasswordView(View):
    def post(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        username = request.session.get("username")
        old_password = request.POST.get("old_password")
        new_password = request.POST.get("new_password")
        user = authenticate(request, username=username, password=old_password)
        if not user:
            return HttpResponse("原密码错误")
        else:
            user.set_password(new_password)
            user.save()
            return HttpResponse("ok")


def order_info_manage_view(request):
    return render(request, "order_info_manage.html")


class ShopCartView(View):
    def get(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        else:
            username, services_sort, is_login = Util.get_basic_info(request)
            username = request.session.get("username")
            user = User.objects.filter(username=username)[0]
            u_id = user.id
            carts = Cart.objects.filter(user_id=u_id)
            total_cost = 0
            for cart in carts:
                total_cost += cart.service.price
            cart_size = len(carts)
            return render(request, "shop_cart.html",
                          {"user": user, "carts": carts, "cart_size": cart_size, "total_cost": total_cost,"username":username,"services_sort":services_sort,"is_login":is_login})

    def post(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        else:
            username = request.session.get("username")
            user = User.objects.filter(username=username)[0]
            service_id = int(request.POST.get("service_id"))
            u_id = user.id
            carts = Cart.objects.filter(user_id=u_id)
            for cart in carts:
                if cart.service.id == service_id:
                    Cart.objects.filter(id=cart.id).delete()
            return self.get(request)


class VendorInfoManageView(View):
    def get(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        else:
            username, services_sort, is_login = Util.get_basic_info(request)
            username = request.session.get("username")
            user = User.objects.filter(username=username)[0]
            shop = Shop.objects.filter(user_id=user.id)[0]
            services = Service.objects.filter(shop_id=shop.id)
            order_list = []
            for service in services:
                order_list.extend(Order.objects.filter(service_id=service.id))

            return render(request, "vendor_info_manage.html", {"user": user, "shop": shop, "order_list": order_list,"username":username,"services_sort":services_sort,"is_login":is_login})


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
