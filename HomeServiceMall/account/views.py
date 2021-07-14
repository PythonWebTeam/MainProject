from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views import View
from account.models import *
from utils.util import Util


class UserInfoManageView(View):
    def get(self, request, msg=""):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        username, services_sort, is_login = Util.get_basic_info(request)
        username = request.session.get("username")
        user = User.objects.get(username=username)
        if user.is_vendor:
            return redirect("/accountendorsendor_info_manage")
        order_list = Order.objects.filter(user_id=user.id)
        addr = Util.transform(user.province, user.city, user.district)
        return render(request, "user_info_manage.html",
                      {"user": user, "order_list": order_list, "username": username, "services_sort": services_sort,
                       "is_login": is_login, "prov": addr[0], "city": addr[1], "county": addr[2], "msg": msg})

    def post(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        data = request.POST
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        username = request.session.get("username")
        user = User.objects.get(username=username)
        Order.objects.filter(user_id=user.id)
        new_username = data.get("username")  #
        if User.objects.filter(username=new_username):
            msg = "该用户名已存在"
            return render(request, "user_info_manage.html",
                          {"user": user, "order_list": order_list, "msg": msg, "username": username,
                           "services_sort": services_sort, "is_login": is_login})
        phone = data.get("phone")  #
        fChangeTrue = data.get("ChangeAddr")  #
        if fChangeTrue == 0:
            user.username = new_username
            user.phone = phone
        else:
            user.prov = int(data.get("prov"))
            user.city = int(data.get("city"))
            user.county = int(data.get("county"))

            user.details = data.get("addr")
            print(user.prov, user.city, user.county, user.details)
            print(user.prov, user.city, user.county, user.details)

            user.save()
        return self.get(request)


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
                          {"user": user, "carts": carts, "cart_size": cart_size, "total_cost": total_cost,
                           "username": username, "services_sort": services_sort, "is_login": is_login})

    def post(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        else:
            username = request.session.get("username")
            user = User.objects.filter(username=username)[0]
            service_id = int(request.POST.get("service_id"))
            carts = Cart.objects.filter(user=user)
            for cart in carts:
                if cart.service.id == service_id:
                    Cart.objects.filter(id=cart.id)[0].delete()
            return self.get(request)


class CartRemoveAll(View):
    def post(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        else:
            username = request.session.get("username")
            user = User.objects.filter(username=username)[0]
            carts = Cart.objects.filter(user=user)
            if carts:
                for cart in carts:
                    Cart.objects.get(id=cart.id).delete()
                return redirect("/account/users/shop_cart")
            else:
                return redirect("/account/users/shop_cart")


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
            response_data = {
                "user": user,
                "shop": shop,
                "order_list": order_list,
                "username": username,
                "services_sort": services_sort,
                "is_login": is_login
            }
            return render(request, "vendor_info_manage.html", response_data)


class DeleteService(View):
    def post(self, request):
        data = request.POST.get
        service_name = data.get("service_name")
        s_id = int(data.get("s_id"))
        search_dict = dict()
        search_dict["service_name"] = service_name
        search_dict["s_id"] = s_id
        service = Service.objects.filter(**search_dict)
        if not service:
            return HttpResponse("您要删除的服务不存在")
        else:
            Service.objects.get(**search_dict).delete()
            return HttpResponse("ok")


def product_manage_view(request):
    return render(request, "product_manage.html")


def order_manage_view(request):
    return render(request, "order_manage.html")


def service_manage_view(request):
    return render(request, "service_manage.html")


class BusinessDataView(View):
    def get(self, request):
        # 通过session获取用户信息
        vendor_name = request.session.get("username")
        vendor = User.objects.get(username=vendor_name)
        # 判断是否为商家
        if not vendor.is_vendor:
            return HttpResponse("您不是商家，请申请成为商家")
        # 获取近几个月的订单数据
        recent_months_orders = self.get_recent_month_orders_data(vendor)
        # 获取近30天的不同类型订单数据
        current_month_orders = self.get_current_month_orders_data(vendor)
        # 以json形式返回响应
        json_data = {
            "recent_months_orders": recent_months_orders,
            "current_month_orders": current_month_orders
        }
        # 将safe设为False以便序列化列表
        return JsonResponse(json_data, safe=False)

    def get_current_month_orders_data(self, vendor):
        # 获取vendor的id
        vendor_id = vendor.id
        now_time = datetime.now()
        # 通过id找到
        shop = Shop.objects.get(id=vendor_id)
        shop_orders = self.get_total_orders(shop)
        all_type = Type.objects.all()
        data_by_type = dict()
        for service_type in all_type:
            init_type_dict = {service_type: 0}
            data_by_type.update(init_type_dict)
        for order in shop_orders:
            if (now_time - order.create_time).days < 30:
                data_by_type = data_by_type.get(
                    order.service.sort.name, 0) + 1  # TODO:可简化
        return data_by_type

    def get_recent_month_orders_data(self, vendor):
        vendor_id = vendor.id
        now_time = datetime.now()
        shop = Shop.objects.get(id=vendor_id)
        shop_orders = self.get_total_orders(shop)
        order_month_list = [0, 0, 0, 0, 0, 0]
        for order in shop_orders:
            month = (now_time - order.create_time).days // 30
            if month < 6:
                order_month_list[month] += 1
        recent_month_data = dict()
        for month in range(0, 6):
            month_name = "距今第{}月内".format(month + 1)
            sales = order_month_list[month]
            info = {month_name: sales}
            recent_month_data.update(info)
        return recent_month_data

    def get_one_kind_orders(self, service):
        return Order.objects.filter(service_id=service.id)

    def get_total_orders(self, shop):
        shop_services = Service.objects.filter(shop_id=shop.id)
        shop_orders = []
        for service in shop_services:
            one_kind_orders = self.get_one_kind_orders(service)
            shop_orders.extend(one_kind_orders)
        return shop_orders


class AppendService(View):
    def post(self, request):
        pass
