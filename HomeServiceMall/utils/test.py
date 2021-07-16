import datetime
import time

from django.http import HttpResponse
from django.shortcuts import render
import random
from account.models import Service, User, Shop, Order

comment = ["终于收到我需要的宝贝了，东西很好，价美物廉，谢谢掌柜的!说实在，这是我淘宝购物来让我最满意的一次购物。",
           "掌柜态度很专业热情，有问必答，回复也很快",
           "质量非常好，与卖家描述的完全一致，非常满意,真的很喜欢，完全超出期望值，发货速度非常快",
           "不好意思评价晚了，非常好的店家，东西很喜欢！买来这个是送人的她很喜欢卖家的贴心让我感到很温暖",
           "很热情的卖家，下次还来希望下次还有机会合作祝你生意兴隆质量非常好真出乎我的意料包装非常仔细非常感谢。祝生意兴隆",
           "物流公司的态度比较差,建议换一家！不过掌柜人还不错！",
           "很好的卖家，谢谢喽。我的同事们都很喜欢呢。下次再来哦！",
           "掌柜人不错，质量还行，服务很算不错的。",
           "本人对此卖家之仰慕如滔滔江水连绵不绝，海枯石烂，天崩地裂，永不变心",
           "交易成功后，我的心情竟是久久不能平静。自古英雄出少年，卖家年纪轻轻，就有经天纬地之才，定国安邦之智",
           "这么好的卖家，如果将来我再也遇不到了，那我该怎么办？直到我毫不犹豫地把卖家的店收藏了，我内心的那种激动才逐渐平静下来",
           "经过痛苦的思想斗争，我终于下定决心，牺牲小我，奉献大我。我要以此评价奉献给世人赏阅，我要给好评",
           ]


def pay_test_view(request):
    return render(request, "result.html", {"result": "支付成功"})


def test_view(request):
    all_users = User.objects.all()
    all_services = Service.objects.all()
    all_shops = Shop.objects.all()
    name = "赵钱孙李周吴郑王冯陈褚卫蒋沈韩国人类原朝和五代的时候很多少数民族的统治者和汉族同始社会的母系氏族制时期杨朱秦尤许何吕施张孔曹严华金魏陶姜戚谢邹喻柏水窦章云苏潘葛奚范彭郎"
    number = "0123456789"
    number_char = "0123456789abcdefghijklmnopqrstuvwxyz"
    email_ = "@qq.com"
    for i in range(100):
        timestamp = 1626434656514
        timerange = random.randint(0, 13434656514)

        # 转换成localtime
        time_local = time.localtime((timestamp - timerange) / 1000)
        # 转换成新的时间格式(精确到秒)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)

        order = Order()
        order.service = all_services[random.randint(0, len(all_services) - 1)]
        order.user = all_users[random.randint(0, len(all_users) - 1)]
        order.create_time = dt
        timerange = random.randint(0, 13434656514)

        # 转换成localtime
        time_local = time.localtime((timestamp - timerange) / 1000)
        # 转换成新的时间格式(精确到秒)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        order.start_time = dt
        timerange = random.randint(0, 13434656514)

        # 转换成localtime
        time_local = time.localtime((timestamp - timerange) / 1000)
        # 转换成新的时间格式(精确到秒)
        dt = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        order.end_time=dt
        order.comment = comment[random.randint(0, len(comment) - 1)]
        order.star = random.randint(2, 5)
        psw = ""
        order.pay_status = 1
        for j in range(16):
            psw = psw + number_char[random.randint(0, len(number_char) - 1)]
        order.order_collection_id = psw
        order.save()

        # name_len = random.randint(2, 3)
        # username = ""
        # for j in range(name_len):
        #     username = username + name[random.randint(0,len(name)-1)]
        # phone=""
        # for j in range(11):
        #     phone=phone+number[random.randint(0,len(number)-1)]
        # email=""
        # psw=""
        # for j in range(16):
        #     email=email+number_char[random.randint(0,len(number_char)-1)]
        #     psw=psw+number_char[random.randint(0,len(number_char)-1)]
        # email+=email_
        #
        # print(username,phone,email,psw)
    all_orders = Order.objects.all()
    print(len(all_users), len(all_services), len(all_shops), len(all_orders))
    return HttpResponse("OK")
