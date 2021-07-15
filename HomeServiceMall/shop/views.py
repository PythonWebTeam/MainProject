import datetime

from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from account.models import Service, User, Cart, Shop
from utils.util import Util


class ServiceView(View):
    def get(self, request):
        username, services_sort, is_login = Util.get_basic_info(request)
        se_id = request.GET.get("se_id")
        service = Service.objects.filter(id=int(se_id))[0]
        return render(request, "service.html",
                      {"service": service, "username": username, "services_sort": services_sort, "is_login": is_login})

    def post(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        data = request.POST
        se_id = int(data.get("se_id"))
        username = request.session.get("username")
        user = User.objects.filter(username=username)[0]
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        start_time = datetime.datetime.strptime(start_time, "%Y-%m-%dT%H:%M")
        end_time = datetime.datetime.strptime(end_time, "%Y-%m-%dT%H:%M")
        CartNum = len(Cart.objects.filter(user=user))
        service=Service.objects.get(id=se_id)
        if CartNum >= 10:
            return HttpResponse("购物车最多添加10件服务")
        u_id = user.id
        carts = Cart.objects.filter(user_id=u_id)
        exist = False
        for cart in carts:
            if cart.service.id == se_id:
                exist = True
        if not exist:
            CartAdd = Cart()
            CartAdd.service = service
            CartAdd.user = user
            CartAdd.start_time = start_time
            CartAdd.end_time = end_time
            CartAdd.save()
            return HttpResponse("ok")
        else:
            if start_time == cart.start_time and end_time == cart.end_time:
                return HttpResponse("已添加该服务")
            else:
                cart.start_time = start_time
                cart.end_time = end_time
                cart.save()
                return HttpResponse("购物车该服务时间修改成功")


class ShopView(View):
    def get(self, request):
        username, services_sort, is_login = Util.get_basic_info(request)
        data = request.GET
        s_id = int(data.get("s_id"))
        page_num = int(data.get("page"))
        shop = Shop.objects.get(id=s_id)
        services = Service.objects.filter(shop_id=s_id)
        per_page = 12
        paginator = Paginator(services, per_page)
        curr_page = paginator.page(page_num)
        response_data = {
            "username": username,
            "services_sort": services_sort,
            "is_login": is_login,
            "shop": shop,
            "curr_page": curr_page,
            "paginator": paginator
        }
        return render(request, "shop.html", response_data)


class PayView(View):
    def get(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")
        username, services_sort, is_login = Util.get_basic_info(request)
        se_id = request.GET.get("se_id")
        from_cart = request.GET.get("from_cart")
        username = request.session.get("username")
        user = User.objects.filter(username=username)[0]
        if int(from_cart) == 0:
            services = Service.objects.filter(id=int(se_id))
        else:
            carts = Cart.objects.filter(user_id=user.id)
            services = []
            for cart in carts:
                services.append(cart.service)
        total_cost = 0
        for service in services:
            total_cost += service.price
        # 获取用户的地址信息
        addr = Util.transform(user.province, user.city, user.district)
        return_data = {
            "services": services,
            "total_cost": total_cost,
            "user": user,
            "username": username,
            "services_sort": services_sort,
            "is_login": is_login,
            "prov": addr[0],
            "city": addr[1],
            "county": addr[2],
            "from_cart": from_cart,
        }
        return render(request, "pay.html", return_data)
