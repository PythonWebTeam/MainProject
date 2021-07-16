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
        order_key = "price"
        page_num = int(request.GET.get("page"))
        services = []
        if order_by:
            if int(order_by) == 1:
                order_key = "price"
            else:
                order_key = "-sales"
        if key =="" or key is None:
            services = Service.objects.filter().order_by(order_key)
        else:
            type_id = Type.objects.filter(name__contains=key)  # 通过关键字找该类服务id
            services = Service.objects.filter(name__contains=key)
            if type_id:
                type_id = type_id[0]
                services = Service.objects.filter(sort=type_id).order_by(order_key)  # 通过id找出所有满足关键字的服务

        per_page = 12
        paginator = Paginator(services, per_page)
        curr_page = paginator.page(page_num)
        return render(request, "services_class.html",
                      {"curr_page": curr_page, "paginator": paginator, "key": key,
                       "username": username, "services_sort": services_sort, "is_login": is_login, "order_by": order_by})
