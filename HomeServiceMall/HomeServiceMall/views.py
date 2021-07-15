from django.shortcuts import render, redirect
from django.views import View
from account.models import Service, User, Type
from utils.util import Util


class HomeView(View):

    def get(self, request):
        username, services_sort, is_login = Util.get_basic_info(request)
        # 获取所有服务销量

        services_sales = Service.objects.order_by("sales")
        top_service = services_sales.reverse()[:8]
        return render(request, "home.html",
                      {"username": username, "services_sort": services_sort, "top_service": top_service,
                       "is_login": is_login})

    def post(self, request):
        return self.get(request)


def page_not_found(request, exception):
    return render(request, "404.html")
