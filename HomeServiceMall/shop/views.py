from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def service_view(request,service):
    return render(request,"service.html",{"msg":service})

def shop_view(request):
    return render(request,"shop.html")
def pay_view(request,service):
    return render(request,"pay.html",{"msg":service})