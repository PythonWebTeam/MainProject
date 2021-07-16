import time
from datetime import datetime

from django.contrib.auth import authenticate
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.http import HttpResponse
from django.shortcuts import redirect

from HomeServiceMall import settings
from utils.province import province


class User(AbstractUser):
    phone = models.CharField(verbose_name='用户电话', max_length=32, unique=True, blank=True, null=True)
    province = models.IntegerField(verbose_name='省份', blank=True, null=True)
    city = models.IntegerField(verbose_name='城市', blank=True, null=True)
    district = models.IntegerField(verbose_name='区县', blank=True, null=True)
    details = models.CharField(verbose_name='详细地址', max_length=255, blank=True, null=True)
    mod_date = models.DateTimeField(verbose_name='Last modified', null=True, auto_now=True)
    is_vendor = models.BooleanField(verbose_name="商贩", default=0)

    class Meta:
        db_table = 'auth_user'

    def __str__(self):
        return self.username

    def __unicode__(self):
        return self.username

    # 在session中写入数据
    def set_session_login(self, request):
        request.session["is_login"] = True
        request.session["username"] = self.username

    # 检查是否登录，没有登录则重定向至登录页面
    @staticmethod
    def login_check(request):
        if not request.session.get("is_login"):
            return redirect("/passport/login/")

    # 将用户登录进入登录态,返回登录信息
    @staticmethod
    def login(request):
        username = request.POST.get("user-name")
        password = request.POST.get("user-password")
        user = authenticate(request, username=username, password=password)
        if user:
            if user.is_superuser:
                return HttpResponse("您的账户为管理员账户，请从管理员界面登录")
            user.set_session_login(request)
            return HttpResponse("ok")
        else:
            return HttpResponse("账号或密码错误!")

    # 修改用户名
    def change_username(self, request, new_username):
        self.username = new_username
        request.session["username"] = new_username
        self.save()

    # 修改密码
    def change_password(self, new_password):
        self.set_password(new_password)
        self.save()

    # 获取用户所有订单
    def get_all_orders(self):
        orders = Order.objects.filter(user_id=self.id)
        return orders

    # 获取用户购物车信息
    def get_cart(self):
        carts = Cart.objects.filter(user_id=self.id)
        return carts

    # 上传头像
    def upload_portrait_img(self, request):
        try:
            # 获取上传的图片
            pic = request.FILES["picture"]
            now = datetime.now()

            time_str = "{}年{}月{}日{}时{}分{}秒".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
            # 以带时间格式创建一个文件
            file_url = '%s/portrait/%s_%s' % (settings.MEDIA_ROOT, time_str, pic.name)

            with open(file_url, "wb") as f:
                # 获取上传文件内容并写入创建文件中
                for content in pic.chunks():
                    f.write(content)
            # 在数据库中保存上传记录
            self.img = "img/%s" % pic.name
            return True
        except:
            print("error")
            return False

    # 将地址代码转换为文字
    def transform_address(self):
        dict_prov = province[self.province]
        str_prov = dict_prov.get("name")
        dict_city = dict_prov.get("city")[self.city]
        str_city = dict_city.get("name")
        str_county = dict_city.get("districtAndCounty")[self.district]
        return str_prov, str_city, str_county


class Cart(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)  # 联接Service表
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 联接User表
    start_time = models.DateTimeField('设置服务开始时间', null=True)
    end_time = models.DateTimeField('设置服务结束时间', null=True)

    class Meta:
        db_table = 'Cart'

    def __str__(self):
        return str(self.user) + ":" + str(self.service)

    def __unicode__(self):
        return str(self.user) + ":" + str(self.service)

    # 获取购物车的时长
    def get_cart_hour(self):
        delta_time = self.end_time - self.start_time
        delta_seconds = delta_time.total_seconds()
        delta_hours = delta_seconds / 3600
        return delta_hours

    # 获取购物车的价格
    def get_cart_price(self):
        delta_time = self.end_time - self.start_time
        delta_seconds = delta_time.total_seconds()
        delta_hours = delta_seconds / 3600
        service_price = float(self.service.price)
        total_cost = delta_hours * service_price
        return total_cost


class Order(models.Model):
    service = models.ForeignKey('Service', null=True, blank=True, on_delete=models.SET_NULL)  # 联接Service表
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # 联接User表
    create_time = models.DateTimeField('订单创建时间')
    start_time = models.DateTimeField('服务开始时间')
    end_time = models.DateTimeField('服务结束时间')
    pay_status = models.BooleanField('订单支付状态', default=False)
    comment = models.CharField(verbose_name='评价', max_length=255, blank=True, null=True, default="该用户尚未评价,默认5星好评")
    star = models.IntegerField(verbose_name='服务星级', blank=True, null=True, default=5)
    order_collection_id = models.CharField('OrderCollection', blank=True, null=True, max_length=255)

    class Meta:
        db_table = 'Order'

    def __str__(self):
        return str(self.user) + ":" + str(self.service)

    def __unicode__(self):
        return str(self.user) + ":" + str(self.service)

    # 给该订单设置评价和星级
    def set_comment(self, comment, star):
        msg = ""
        try:
            self.comment = comment
            self.star = star
            self.save()
            msg = "ok"

        except:
            msg = "评论失败"
        finally:
            return msg

    # 获取订单的价格
    def get_order_price(self):
        delta_time = self.end_time - self.start_time
        delta_seconds = delta_time.total_seconds()
        delta_hours = delta_seconds / 3600
        service_price = float(self.service.price)
        order_price = delta_hours * service_price
        return order_price

    # 支付订单
    def pay_order(self):
        if self.pay_status:
            msg = "您已经支付过该订单，请勿重新支付"
            return msg
        else:
            self.pay_status = True
            self.save()
            self.service.sales += 1  # 订单对应服务的销量加1
            self.service.save()
            msg = "支付成功"

    # 获取订单号
    def get_order_no(self):
        return self.order_collection_id

    # 获取同订单号的全部订单
    def get_orders_by_order_no(self):
        orders = Order.objects.filter(order_collection_id=self.get_order_no())
        return orders

    # 订单号生成器
    @staticmethod
    def order_no_generator():
        order_no = "x2" + str(time.time().hex())
        return order_no


class Shop(models.Model):
    name = models.CharField('店铺名称', max_length=32, unique=True)
    create_time = models.DateTimeField('店铺创建时间')
    status = models.BooleanField('店铺状态')
    star = models.IntegerField(verbose_name='店铺星级', blank=True, null=True, default=5)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 联接User表

    class Meta:
        db_table = 'Shop'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    # 获取当前月的全部订单数据
    def get_current_month_orders_data(self):
        now_time = datetime.now()
        shop_orders = self.get_total_orders()
        all_type = Type.objects.all()
        data_by_type = dict()
        for service_type in all_type:
            init_type_dict = {service_type.name: 0}
            data_by_type.update(init_type_dict)
        for order in shop_orders:
            if (now_time - order.create_time).days < 30:
                data_by_type[order.service.sort.name] = data_by_type.get(
                    order.service.sort.name, 0) + 1
        return data_by_type

    # 获取近几个月的全部订单数据
    def get_recent_month_orders_data(self):
        now_time = datetime.now()
        shop_orders = self.get_total_orders()
        order_month_list = [0, 0, 0, 0, 0, 0]
        for order in shop_orders:
            month = (now_time - order.create_time).days // 30
            if month < 6:
                order_month_list[month] += 1
        recent_month_data = dict()
        for month in range(0, 6):
            month_name = "距今第{}月内".format(month + 1)
            sales = order_month_list[month]
            info = {month_name: sales}
            recent_month_data.update(info)

        return recent_month_data

    # 以获取店铺的全部订单
    def get_total_orders(self):
        shop_services = self.get_shop_services()
        shop_orders = []
        for service in shop_services:
            orders = service.get_all_orders()
            shop_orders.extend(orders)
        return shop_orders

    # 获取店铺的所有服务
    def get_shop_services(self):
        shop_services = Service.objects.filter(shop_id=self.id)
        return shop_services

    # 获取店铺的星级
    def get_shop_star(self):
        shop_services = self.get_shop_services()
        stars = 0
        service_num = len(shop_services)
        if service_num == 0:
            return 5
        for service in shop_services:
            stars += service.get_service_star()
        aver_star = stars / service_num
        return aver_star

    # 获取店铺店主的电话号码
    def get_shop_phonenumber(self):
        user = User.objects.get(id=self.user_id)
        phone_num = user.phone
        return phone_num


class Type(models.Model):
    name = models.CharField('服务种类名称', max_length=32)

    class Meta:
        db_table = 'Type'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name

    # 获取所有订单种类
    @staticmethod
    def get_all_sort():
        return Type.objects.all()


class Service(models.Model):
    name = models.CharField('服务名称', max_length=32)
    price = models.DecimalField('服务价格', max_digits=10, decimal_places=2)
    status = models.BooleanField('服务状态')
    img = models.ImageField(upload_to="img", null=True)
    intro = models.CharField('服务简介', max_length=255, blank=True, null=True)
    sales = models.IntegerField("销量", default=0)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)  # 联接Shop表
    sort = models.ForeignKey('Type', on_delete=models.CASCADE)  # 联接Type表

    class Meta:
        db_table = 'Service'

    def __str__(self):
        return '{0}({1})'.format(self.name, self.sort)

    def __unicode__(self):
        return '{0}({1})'.format(self.name, self.sort)

    # 获取服务的图片路径
    def get_img_path(self):
        path = "/static/media/" + str(self.img)
        return path

    # 获取该服务的全部订单
    def get_all_orders(self):
        orders = Order.objects.filter(service_id=self.id)
        return orders

    # 新建服务
    @staticmethod
    def new_service(name, price, intro, shop_id, type_id):
        service = Service.objects.create(name=name, price=price, status=True, intro=intro, shop_id=shop_id,
                                         sort_id=type_id)
        service.save()
        return service

    # 获取服务的星级
    def get_service_star(self):
        orders = Order.objects.filter(service_id=self.id)
        stars = 0
        order_num = len(orders)
        if order_num == 0:
            return 5
        for order in orders:
            if order.star is None:
                continue
            stars += order.star
        aver_star = stars / order_num
        return aver_star

    # 上传服务的图片
    def upload_service_img(self, request):
        try:
            # 获取上传的图片
            pic = request.FILES["picture"]
            now = datetime.now()

            time_str = "{}年{}月{}日{}时{}分{}秒".format(now.year, now.month, now.day, now.hour, now.minute, now.second)
            # 以带时间格式创建一个文件
            file_url = '%s/img/%s_%s' % (settings.MEDIA_ROOT, time_str, pic.name)

            with open(file_url, "wb") as f:
                # 获取上传文件内容并写入创建文件中
                for content in pic.chunks():
                    f.write(content)

            # 在数据库中保存上传记录
            self.img = "img/%s_%s" % (time_str, pic.name)
            self.save()
            return True
        except:
            return False




class EmailVerifyRecord(models.Model):
    # 验证码
    code = models.CharField(max_length=20, verbose_name=u"验证码")
    email = models.EmailField(max_length=50, verbose_name=u"邮箱")
    # 包含注册验证和找回验证
    send_type = models.CharField(verbose_name=u"验证码类型", max_length=10,
                                 choices=(("register", u"注册"), ("forget", u"找回密码")))
    send_time = models.DateTimeField(verbose_name=u"发送时间", default=datetime.now)

    class Meta:
        verbose_name = u"邮箱验证码"
        verbose_name_plural = verbose_name

    def __unicode__(self):
        return '{0}({1})'.format(self.code, self.email)

    # 验证邮箱验证码是否正确
    def verify(self, code):
        if self.code == code:
            return True
        else:
            return False


class ApplyforShop(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 联接User表

    class Meta:
        db_table = 'Apply for Shop'

    def __str__(self):
        return self.user.username
