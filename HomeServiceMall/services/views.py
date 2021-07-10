from django.shortcuts import render

# Create your views here.
from django.views import View

from account.models import Service, Type


class ServicesClassView(View):
    def get(self, request):
        # 获取服务列表页面
        key = request.GET.get("search")
        type_id = Type.objects.filter(name__contains=key)  # 通过关键字找该类服务id
        services = []
        if type_id:
            type_id = type_id[0]
            services = Service.objects.filter(sort=type_id)  # 通过id找出所有满足关键字的服务
        services_num = len(services)
        return render(request, "services_class.html", {"services": services, "services_num": services_num})

    def post(self, request):
        pass
