
from random import Random  # 用于生成随机码
from django.core.mail import send_mail  # 发送邮件模块
from django.shortcuts import render
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


def send_register_email(request):  # email, send_type="register"
    # 将给用户发的信息保存在数据库中
    email='1271503697@qq.com'
    code = random_str(4)
    flag=EmailVerifyRecord.objects.filter(email=email)
    if flag:
        flag[0].code=code
        flag[0].save()

    else:
        email_record = EmailVerifyRecord()
        email_record.code = code
        email_record.email = '1271503697@qq.com'
        email_record.send_type = "register"
        email_record.save()
    # 初始化为空
    email_title = ""
    email_body = ""
    # 如果为注册类型
    email_title = "注册激活链接"
    # email_body = "请点击下面的链接激活你的账号:http://127.0.0.1:8000/active/?code={0}&email={1}\n" \
    email_body = "验证码为{0}".format(code)
    # 发送邮件
    send_status = send_mail(email_title, email_body, EMAIL_FROM,[email])
    if send_status:
        pass
    return render(request, "test.html")


# def active(request):
#     code1=request.GET.get("code")
#     email=request.GET.get("email")
#     code2=EmailVerifyRecord.objects.filter(email=email)[0]
#
#
#     if code1 == code2.code:
#         msg = '验证成功'
#     else:
#         msg="验证失败"
#     return render(request, "active.html", {'msg':msg})'''