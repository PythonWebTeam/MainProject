from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views import View

from account.models import Service


class ServiceView(View):
    def get(self, request):
        se_id = request.GET.get("se_id")
        service = Service.objects.filter(id=int(se_id))

        return render(request, "service.html", {"service": service[0]})


class ShopView(View):
    def get(self, request):
        return render(request, "shop.html")


class PayView(View):
    def get(self,request):
        se_id = request.GET.get("se_id")
        print(se_id)
        service = Service.objects.filter(id=int(se_id))
        return render(request, "pay.html",{"service":service})
