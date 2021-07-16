import datetime
import time
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from HomeServiceMall import settings
from django.shortcuts import render, redirect
import decimal
from account.models import User, Cart, Service, Order
from utils.pay import AliPay
from utils.recommend import recommend
from utils.util import Util


def aliPay():
    obj = AliPay(
        appid="2021000117687494",  # 支付宝沙箱里面的APPID，需要改成你自己的
        app_notify_url="http://127.0.0.1:8000/shop/service/pay/update/",
        # 如果支付成功，支付宝会向这个地址发送POST请求（校验是否支付已经完成），此地址要能够在公网进行访问，需要改成你自己的服务器地址
        return_url="http://127.0.0.1:8000/shop/service/pay/result/",  # 如果支付成功，重定向回到你的网站的地址。需要你自己改，这里是我的服务器地址
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


def convert_digital_decimal(value):
    # 判断decimal类型
    if type(value) is type(decimal.Decimal.from_float(0.0)):
        # 转换
        return float(value.quantize(decimal.Decimal('0.00000000000')))
    else:
        return value


def get_delta_hours(start_time, end_time):

    delta_seconds = (end_time - start_time).total_seconds()
    delta_hours = delta_seconds/ 3600
    return delta_hours


@csrf_exempt
def alipay_index(request):
    # 实例化SDK里面的类AliPay
    alipay = aliPay()
    # 对购买的数据进行加密
    data = request.GET
    print(data)
    username = request.session.get("username")
    user = User.objects.get(username=username)
    user_id = user.id
    services_num = 0
    order_code = Order.order_no_generator()
    total_cost = 0
    if int(data.get("from_cart")) == 1:
        carts = Cart.objects.filter(user_id=user_id)
        if not carts:
            return HttpResponse("购物车为空")
        for cart in carts:
            order = Order()
            order.service = cart.service
            price = convert_digital_decimal(cart.service.price)
            print(cart.start_time, cart.end_time)
            total_cost += cart.get_cart_price()
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
        start_time_str = data.get("start_time")
        end_time_str = data.get("end_time")
        start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M")
        end_time = datetime.datetime.strptime(end_time_str, "%Y-%m-%dT%H:%M")
        service = Service.objects.get(id=se_id)
        price = convert_digital_decimal(service.price)
        total_cost += price * get_delta_hours(start_time, end_time)
        order = Order()
        order.service = service
        order.create_time = datetime.datetime.now()
        order.start_time = start_time
        order.end_time = end_time
        order.order_collection_id = order_code
        order.user = user
        order.save()
        services_num += 1
    print(total_cost)
    # 1. 在数据库创建一条数据：状态（待支付）
    query_params = alipay.direct_pay(
        subject="服务名:{0}({1})|共{2}个服务".format(service.name, service.sort.name, services_num),  # 商品简单描述 这里一般是从前端传过来的数据
        out_trade_no=order_code,  # 商户订单号  这里一般是从前端传过来的数据
        total_amount=total_cost,  # 交易金额(单位: 元 保留俩位小数)   这里一般是从前端传过来的数据
    )

    # 拼接url，转到支付宝支付页面
    pay_url = "https://openapi.alipaydev.com/gateway.do?{}".format(query_params)
    print("pay_url")
    return redirect(pay_url)


# TODO:取消注释
'''
@csrf_exempt
def update_order(request):
    """
    支付成功后，支付宝向该地址发送的POST请求（用于修改订单状态）
    :param request:
    :return:
    """
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
        orders = Order.objects.filter(order_collection_id=out_trade_no)
        for order in orders:
            order.pay_status = True
            order.save()
        # 2. 根据订单号将数据库中的数据进行更新
        return HttpResponse('支付成功')
    else:
        return HttpResponse('支付失败')

'''


@csrf_exempt
def pay_result(request):
    """
    支付完成后，跳转回的地址
    :param request:
    :return:
    """
    params = request.GET.dict()
    sign = params.pop('sign', None)
    username, services_sort, is_login = Util.get_basic_info(request)
    alipay = aliPay()
    status = alipay.verify(params, sign)
    out_trade_no = params.get('out_trade_no')
    recommend_services_all=[]
    if status:
        orders = Order.objects.filter(order_collection_id=out_trade_no)
        for order in orders:
            order.pay_order()
            recommend_services = recommend(order.service,count=12)
            for service in recommend_services:
                if service not in recommend_services_all:
                    recommend_services_all.append(service)
        if not len(recommend_services_all):
            recommend_info="暂无推荐"
        else:
            recommend_info = "购买了该商品的用户还购买了:"
        data={
            "username": username,
            "services_sort": services_sort,
            "is_login": is_login,
            "result":"支付成功",
            "services":recommend_services_all,
            "recommend_info":recommend_info
        }
        return render(request, "result.html" , data)
    data={
        "result":"支付失败,请重新购买",
        "username": username,
        "services_sort": services_sort,
        "is_login": is_login,
        }
    return render(request, "result.html" , data)
# http://127.0.0.1:8000/shop/service/pay/result/?charset=utf-8&out_trade_no=x21626277188.7983813&method=alipay.trade.page.pay.return&total_amount=100.00&sign=hxzf0A6pNL8WDB8Q6vSJ%2FyAaFlhO8hxFCd4CBsqs7bMTtSCRQ%2FfEhqdtve7wzoF0T%2FByhQkpdyoPYpqcF54clxdEpIJfUCPdK4paw1vlnSV5bEzdZgLD5PLRoIEtZTN0V1J72uOpFEB%2Brmq1FGTLayCBh9zjG46D7hNu62pEv9p12bIvmwtolYT%2FPvy9r0F1hODw1whTG%2Fpwk574IAwEubA%2FOr93nJ3S9X8wtEPE4ESEtHwmEc8%2FHRCMH2zZhwq9tLwVjtZemLzEa56%2B0xkdVPBskeDpVxGjJ%2BWw5KclqfXRUPF5BFelL7WrO%2BGevKNfrHS2zrkh5KwU4d7VDT6EWw%3D%3D&trade_no=2021071422001457990501358213&auth_app_id=2021000117687494&version=1.0&app_id=2021000117687494&sign_type=RSA2&seller_id=2088621956124101&timestamp=2021-07-14+23%3A40%3A13
