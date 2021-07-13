from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from account.models import Service, EmailVerifyRecord
from utils.util import Util

User = get_user_model()


# 登录页面视图
class LoginView(View):
    def get(self, request):
        if request.session.get("is_login"):
            return HttpResponse("用户 " + request.session.get("username") + ",您已登录")
        username, services_sort, is_login = Util.get_basic_info(request)
        return render(request, "login.html",
                      {"username": username, "services_sort": services_sort, "is_login": is_login})

    def post(self, request):

        username = request.POST.get("user-name")
        password = request.POST.get("user-password")
        user = authenticate(request, username=username, password=password)
        if user:
            request.session["is_login"] = True
            request.session["username"] = username
            return HttpResponse("ok")
        else:
            return HttpResponse("账号或密码错误!")


class RegisterView(View):
    def get(self, request):
        return HttpResponse("404 not found")

    def post(self, request):

        data = request.POST
        print(data)
        username = data.get("user-name")
        password = data.get("user-password")
        phone_number = data.get("phone-number")
        email = data.get("user-email")
        addr = data.get("address")
        prov = data.get("prov")
        city = data.get("city")
        county = data.get("county")
        if User.objects.filter(username=username):
            return HttpResponse('用户名已被注册')
        elif User.objects.filter(phone=phone_number):
            return HttpResponse("该手机号已被注册")
        code_rec = data.get("email_code")
        if not EmailVerifyRecord.objects.filter(email=email):
            return HttpResponse("请获取验证码并验证邮箱")
        code_db = EmailVerifyRecord.objects.filter(email=email)[0].code
        if code_rec != code_db:
            return HttpResponse("邮箱验证码错误")
        user = User.objects.create_user(username=username, password=password, phone=phone_number, email=email,
                                        province=prov, district=county, details=addr, city=city)
        if user:
            return HttpResponse("ok")


class RetrieveView(View):
    def get(self, request):
        username, services_sort, is_login = Util.get_basic_info(request)
        return render(request, "retrieve.html",
                      {"username": username, "services_sort": services_sort, "is_login": is_login})

    def post(self, request):
        username = request.POST.get("username")
        email = request.POST.get("email")
        code_rec = request.POST.get("email_code")
        new_password = request.POST.get("new_password")
        users = User.objects.filter(username=username)
        if not users:
            return HttpResponse("此用户不存在")
        else:
            user = users[0]
            if not EmailVerifyRecord.objects.filter(email=email):
                return HttpResponse("请获取验证码并验证邮箱")
            code_db = EmailVerifyRecord.objects.filter(email=email)[0].code
            if code_rec != code_db:
                return HttpResponse("邮箱验证码错误")
            user.set_password(new_password)
            user.save()
            return HttpResponse("ok")


class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect("/")
