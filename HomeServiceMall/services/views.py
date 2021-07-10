from django.shortcuts import render

# Create your views here.
from django.views import View

from account.models import Service


class ServicesClassView(View):
    def get(self, request):
        # 获取服务列表页面
        type_id = request.GET.get("type_id")
        services = Service.objects.filter("type_id")
        services_num = len(services)
        return render(request, "services_class.html", services, services_num)

    def post(self, request):

        pass
