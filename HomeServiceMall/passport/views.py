from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from account.models import EmailVerifyRecord
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
            if user.is_superuser:
                return HttpResponse("您的账户为管理员账户，请从管理员界面登录")
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
        username = data.get("user-name")
        password = data.get("user-password")
        phone_number = data.get("phone-number")
        email = data.get("user-email")
        address = data.get("address")
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
        email_verify = EmailVerifyRecord.objects.get(email=email)
        if not email_verify.verify(code_rec):
            return HttpResponse("邮箱验证码错误")
        user = User.objects.create_user(username=username, password=password, phone=phone_number, email=email,
                                        province=prov, district=county, details=address, city=city)
        if user:
            return HttpResponse("ok")


class LogoutView(View):
    def get(self, request):
        request.session.flush()
        return redirect("/")


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
        users = User.objects.get(username=username)
        if not users:
            return HttpResponse("此用户不存在")
        elif users.email != email:
            return HttpResponse("邮箱不匹配")
        else:
            user = users
            if not EmailVerifyRecord.objects.filter(email=email):
                return HttpResponse("请获取验证码并验证邮箱")
            code_db = EmailVerifyRecord.objects.get(email=email).code
            if code_rec != code_db:
                return HttpResponse("邮箱验证码错误")
            user.set_password(new_password)
            user.save()
            return HttpResponse("ok")
