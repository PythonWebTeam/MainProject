from datetime import datetime

from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from account.models import EmailVerifyRecord  # 邮箱验证model
from HomeServiceMall.settings import EMAIL_FROM  # setting.py添加的的配置信息


# 生成随机字符串

def random_str(randomlength=8):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


class SendEmailView(View):  # email, send_type="register"
    def post(self, request):


        # 将给用户发的信息保存在数据库中
        email = request.POST.get("email")
        type = request.POST.get("operate_type")  # forget register


        code = random_str(6)
        flag = EmailVerifyRecord.objects.filter(email=email)

        if flag:
            flag=flag[0]
            t1 = flag.send_time
            t1 = t1.replace(tzinfo=None)
            t2 = datetime.datetime.now()
            if (t2 - t1).seconds < 60:
                return HttpResponse("请求发送过快，请{}s之后尝试".format(60 - (t2 - t1).seconds))
            flag.code = code
            flag.send_time = datetime.now
            flag.save()
        else:
            email_record = EmailVerifyRecord()
            email_record.code = code
            email_record.send_type = type
            email_record.email = email
            email_record.save()
        # 如果为注册类型
        if type == "register":
            msg = "注册"
        elif type == "forget":
            msg = "找回密码"
        else:
            msg = ""
        email_title = "Let's 购|{0}-验证码".format(msg)
        email_body = "验证码为{0}".format(code)
        # 发送邮件
        send_status = send_mail(email_title, email_body, EMAIL_FROM, [email])
        if not send_status:
            return HttpResponse("发送失败")
        return HttpResponse("ok")

