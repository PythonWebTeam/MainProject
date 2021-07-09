from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from django.views import View
from account.models import Service, User


class HomeView(View):
    def get(self, request):
        services_sales = Service.objects.order_by("sales")
        top_service = services_sales[:8]
        services_sort = []
        for service in services_sales:
            if service.sort not in services_sort:
                services_sort.append(service.sort)
        return render(request, "home.html", {"services_sort": services_sort, "top_service": top_service})

    def post(self, request):
        pass
