from django.http import HttpResponse
from django.shortcuts import render

from account.models import Service

def pay_test_view(request):
    return render(request,"pay.html",{"result":"支付成功"})
def test_view(request):
    services = Service.objects.all()
    for service in services:
        path = service.img1
        print(path)
    return HttpResponse("ok")
