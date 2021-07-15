from django.core.paginator import Paginator
from django.shortcuts import render
from django.views import View
from account.models import Service, Type
from utils.util import Util


class ServicesClassView(View):
    def get(self, request):
        username, services_sort, is_login = Util.get_basic_info(request)
        # 获取服务列表页面
        key = request.GET.get("search")
        order_by = request.GET.get("Order_by")
        if order_by == 2:
            order_key = "-price"
        else:
            order_key = "-sales"
        type_id = Type.objects.filter(name__contains=key)  # 通过关键字找该类服务id
        page_num = int(request.GET.get("page"))
        services = []

        if type_id:
            type_id = type_id[0]
            services = Service.objects.filter(sort=type_id).order_by(order_key)  # 通过id找出所有满足关键字的服务

        per_page = 12
        paginator = Paginator(services, per_page)
        curr_page = paginator.page(page_num)

        return render(request, "services_class.html",
                      {"curr_page": curr_page, "paginator": paginator, "key": key,
                       "username": username, "services_sort": services_sort, "is_login": is_login})
