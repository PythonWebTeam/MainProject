from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection
from django.views import View
from account.models import Service, User
import random


class Home_view(View):
    def get(self, request):
        db_top = [0, 2, 3, 5, 7, 6, 1, 4]
        db_service_sort = ["家庭清洁", "保姆服务", "电器维修", "居民搬家", "二手回收", "鲜花绿植", "生活配送", "管道疏通", "开锁换锁", "房屋维修"]
        db_service_name = "李佳晨 徐利停 张靖若 李腾龙 张婉茹 李含晓 周依林 李佳欣 詹仁俊 赵晶 周娟 张旭 张婧雯".split()

        services = []
        for i in range(20):
            services.append(
                Service(db_service_name[random.randint(0, len(db_service_name) - 1)], random.randint(1, 1000),
                        db_service_sort[random.randint(0, len(db_service_sort) - 1)]))

        top_service = [services[se_id] for se_id in db_top]
        return render(request, "home.html", {"services_sort": db_service_sort, "top_service": top_service})

    def post(self, request):
        pass


def test_view(request):
    print_all_user()
    return render(request, "test.html")


def print_all_service():
    services = Service.objects.filter()
    for service in services:
        print(service)
def print_all_user():
    users=User.objects.filter()
    for user in users:
        print(user)

