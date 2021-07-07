from django.shortcuts import render, redirect
from django.views import View

# 登录页面视图
class login_view(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        user = request.POST.get("user")
        pwd = request.POST.get("pwd")
        if user == "hofee" and pwd == "123123":
            return redirect("http://www.baidu.com")
        elif len(user) == 0 or len(pwd) == 0:
            if len(user) == 0:
                return render(request, 'login.html', {"msg": "用户名不能为空!"})
            if len(pwd) == 0:
                return render(request, 'login.html', {"msg": "密码不能为空!"})
        else:
            return render(request, 'login.html', {"msg": "用户名或密码错误"})


def register_view(request):
    return render(request, "register.html")


def retrieve_view(request):
    return render(request, "retrieve.html")
