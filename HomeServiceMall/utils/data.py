import datetime
from urllib.parse import parse_qs
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from HomeServiceMall import settings
from django.shortcuts import render, redirect

from account.models import User, Cart, Service, Order
from utils.pay import AliPay


def aliPay():
    obj = AliPay(
        appid="2021000117687494",  # 支付宝沙箱里面的APPID，需要改成你自己的
        app_notify_url="http://127.0.0.1:8000/service/pay/update/",
        # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成），此地址要能够在公网进行访问，需要改成你自己的服务器地址
        return_url="http://127.0.0.1:8000/service/pay/result/",  # 如果支付成功，重定向回到你的网站的地址。需要你自己改，这里是我的服务器地址
        alipay_public_key_path=settings.ALIPAY_PUBLIC,  # 支付宝公钥
        app_private_key_path=settings.APP_PRIVATE,  # 应用私钥

        debug=True,  # 默认False,True表示使用沙箱环境测试
    )

    # 优化:在settings里面的设置后使用
    # obj = AliPay(
    #     appid=settings.APPID,
    #     app_notify_url=settings.NOTIFY_URL,
    #     return_url=settings.RETURN_URL,
    #     alipay_public_key_path=settings.PUB_KEY_PATH,
    #     app_private_key_path=settings.PRI_KEY_PATH,
    #     debug=True,
    # )
    return obj


@csrf_exempt
def alipay_index(request):
    # 实例化SDK里面的类AliPay
    alipay = aliPay()
    # 对购买的数据进行加密
    data = request.POST
    username = request.session.get("username")
    user = User.objects.filter(username=username)[0]
    user_id = user.id
    orders = []
    services_num = 0
    total_cost = float(data.get("cost"))
    order_code = "x2" + str(time.time())
    if int(data.get("from_cart")) == 1:
        carts = Cart.objects.filter(user_id=user_id)
        if not carts:
            return HttpResponse("购物车为空")
        for cart in carts:
            order = Order()
            order.service = cart.service
            order.create_time = datetime.datetime.now()
            order.start_time = cart.start_time
            order.end_time = cart.end_time
            order.order_collection_id = order_code
            order.user = user
            order.save()
            services_num += 1
            service = order.service
        Cart.objects.filter(user_id=user_id).delete()
    else:
        se_id = data.get("se_id")
        start_time = data.get("start_time")
        end_time = data.get("end_time")
        service = Service.objects.filter(id=se_id)[0]
        order = Order()
        order.service = service
        order.create_time = datetime.datetime.now()
        order.start_time = start_time
        order.end_time = end_time
        order.order_collection_id = order_code
        order.user = user
        order.save()
        services_num += 1

    # 1. 在数据库创建一条数据：状态（待支付）
    query_params = alipay.direct_pay(
        subject="服务名:{0}({1})|共{2}个服务".format(service.name, service.sort.name, services_num),  # 商品简单描述 这里一般是从前端传过来的数据
        out_trade_no=order_code,  # 商户订单号  这里一般是从前端传过来的数据
        total_amount=total_cost,  # 交易金额(单位: 元 保留俩位小数)   这里一般是从前端传过来的数据
    )

    # 拼接url，转到支付宝支付页面
    pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
    return redirect(pay_url)


@csrf_exempt
def update_order(request):
    """
    支付成功后，支付宝向该地址发送的POST请求（用于修改订单状态）
    :param request:
    :return:
    """
    if request.method == 'POST':
        body_str = request.body.decode('utf-8')
        post_data = parse_qs(body_str)

        post_dict = {}
        for k, v in post_data.items():
            post_dict[k] = v[0]

        alipay = aliPay()

        sign = post_dict.pop('sign', None)
        status = alipay.verify(post_dict, sign)
        if status:
            # 1.修改订单状态
            out_trade_no = post_dict.get('out_trade_no')
            print(out_trade_no)
            orders=Order.objects.filter(order_collection_id=out_trade_no)
            for order in orders:
                order.pay_status=True
                order.save()
            # 2. 根据订单号将数据库中的数据进行更新
            return HttpResponse('支付成功')
        else:
            return HttpResponse('支付失败')
    return HttpResponse('')


@csrf_exempt
def pay_result(request):
    """
    支付完成后，跳转回的地址
    :param request:
    :return:
    """
    params = request.GET.dict()
    sign = params.pop('sign', None)

    alipay = aliPay()

    status = alipay.verify(params, sign)
    if status:
        return HttpResponse('支付成功')
    return HttpResponse('支付失败')
