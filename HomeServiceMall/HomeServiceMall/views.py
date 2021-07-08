from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from django.views import View

top=[5,1,2,3]
class Services():
    pass
class Home_view(View):
    def get(self,request):
        database = ["家asds", "保姆服务", "服务3", "服务4"]
        return render(request, "home.html", {"services_sort": database})
    def post(self,request):
        pass


