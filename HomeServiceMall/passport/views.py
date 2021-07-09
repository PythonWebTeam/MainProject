from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


# 登录页面视图
class LoginView(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        username = request.POST.get("user-name")
        password = request.POST.get("user-password")

        user = authenticate(request, username=username, password=password)

        if user:
            request.session["is_login"] = True
            request.session["username"] = username
            return redirect("/")
        elif len(username) == 0 or len(password) == 0:
            if len(username) == 0:
                return render(request, 'login.html', {"msg": "用户名不能为空!"})
            if len(password) == 0:
                return render(request, 'login.html', {"msg": "密码不能为空!"})
        else:
            return render(request, 'login.html', {"msg": "用户名或密码错误!"})


class RegisterView(View):
    def get(self, request):
        return render(request, "register.html")


class RetrieveView(View):
    def get(self, request):
        return render(request, "retrieve.html")
