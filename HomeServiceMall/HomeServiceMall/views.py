from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection


def home_view(request):
    database = ["家电维修", "保姆服务", "服务3", "服务4"]
    return render(request, "home.html", {"services_sort": database})
