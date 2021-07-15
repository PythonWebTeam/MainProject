from django.http import HttpResponse
from django.shortcuts import render

from account.models import Service


def pay_test_view(request):
    return render(request, "result.html", {"result": "支付成功"})


def test_view(request):

    return HttpResponse("OK")
