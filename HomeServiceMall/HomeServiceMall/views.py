from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from django.views import View
from account.models import Service, User
import random


class Home_view(View):
    def get(self, request):
        service_sales=Service.objects.order_by("sales")
        top_service=service_sales[:8]
        return render(request, "home.html", {"services_sort":1 , "top_service": top_service})

    def post(self, request):
        pass
