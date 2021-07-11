from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from django.views import View
from account.models import Service, User


class HomeView(View):

    def get(self, request):
        # 判断用户是否已登录
        # TODO:冗余代码
        is_login = request.session.get("is_login", False)
        username = ""
        if is_login:
            username = ":" + request.session.get("username")
        # 获取所有服务销量
        services_sales = Service.objects.order_by("sales")
        # 获取top8热门服务
        top_service = services_sales[:8]
        services_sort = []
        # 获取全部服务种类
        for service in services_sales:
            if service.sort not in services_sort:
                services_sort.append(service.sort)
        return render(request, "home.html",
                      {"username": username, "services_sort": services_sort, "top_service": top_service,
                       "is_login": is_login})

    def post(self, request):

        return self.get(request)
