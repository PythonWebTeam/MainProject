from django.shortcuts import render

from account.models import Service, Type
from utils.province import province


class Util:

    @staticmethod
    def get_basic_info(request):
        # 判断用户是否已登录
        is_login = request.session.get("is_login", False)
        username = ""
        if is_login:
            username = ":" + request.session.get("username")
        # 获取全部服务种类
        services_sort = Type.objects.all()
        return username, services_sort, is_login

    @staticmethod
    def transform(prov, city, county):
        dict_prov = province[prov]
        str_prov = dict_prov.get("name")
        dict_city = dict_prov.get("city")[city]
        str_city = dict_city.get("name")
        str_county = dict_city.get("districtAndCounty")[county]
        return str_prov, str_city, str_county

    @staticmethod
    def login_check(request):
        is_login = request.session.get("is_login", False)
