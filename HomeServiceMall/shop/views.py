from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from account.models import Service, User, Cart


class ServiceView(View):
    def get(self, request):
        se_id = request.GET.get("se_id")
        service = Service.objects.filter(id=int(se_id))[0]
        return render(request, "service.html", {"service": service})


class ShopView(View):
    def get(self, request):
        return render(request, "shop.html")


class PayView(View):
    def get(self, request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")

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
        return render(request, "pay.html", {"services": services, "total_cost": total_cost, "user": user})
