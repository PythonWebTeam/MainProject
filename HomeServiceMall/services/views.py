from django.shortcuts import render

# Create your views here.
from django.views import View


class ServicesClassView(View):
    def get(self,request):
        #获取服务列表页面
        return render(request,"services_class.html")
    def post(self,request):
        pass