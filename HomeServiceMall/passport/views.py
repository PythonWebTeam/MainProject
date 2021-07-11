from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
import datetime
from account.models import Service, EmailVerifyRecord
from utils.util import Util

User = get_user_model()


# 登录页面视图
class LoginView(View):
    def get(self, request):
        if request.session.get("is_login"):
            return HttpResponse("用户 " + request.session.get("username") + ",您已登录")
        return Util.get_page(request, "login.html")

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
        county = data.get("county")

        if User.objects.filter(username=username):
            return HttpResponse('用户名已被注册')
        elif User.objects.filter(phone=phone_number):
            return HttpResponse("该手机号已被注册")
        code_rec = request.GET.get("email_code")
        code_db = EmailVerifyRecord.objects.filter(email=email)[0].code
        if code_rec != code_db:
            return HttpResponse("邮箱验证码错误")
        user = User.objects.create_user(username=username, password=password, phone=phone_number, email=email,
                                        province=prov, district=county, details=addr)
        if user:
            return HttpResponse("ok")


class RetrieveView(View):
    def post(self, request):
        return redirect(request, "passport/login/")
