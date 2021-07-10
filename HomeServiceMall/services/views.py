from django.shortcuts import render

# Create your views here.
from django.views import View

from account.models import Service, Type


class ServicesClassView(View):
    def get(self, request):
        # 获取服务列表页面
        key = request.GET.get("search")
        print(key)
        type_id=Type.objects.filter(name=key)[0]
        services = Service.objects.filter(sort=type_id)
        services_num = len(services)
        print(services)
        return render(request, "services_class.html", {"services": services, "services_num": services_num})

    def post(self, request):
        pass
