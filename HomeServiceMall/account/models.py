from datetime import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser


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


class Order(models.Model):
    service = models.ForeignKey('Service', null=True, blank=True, on_delete=models.SET_NULL)  # 联接Service表
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)  # 联接User表
    create_time = models.DateTimeField('订单创建时间')
    start_time = models.DateTimeField('服务开始时间')
    end_time = models.DateTimeField('服务结束时间')
    pay_status = models.BooleanField('订单支付状态')
    comment = models.CharField(verbose_name='评价', max_length=255, blank=True, null=True)
    star = models.IntegerField(verbose_name='服务星级', blank=True, null=True)
    order_collection_id = models.CharField('OrderCollection', blank=True, null=True, max_length=255)

    class Meta:
        db_table = 'Order'

    def __str__(self):
        return str(self.user) + ":" + str(self.service)

    def __unicode__(self):
        return str(self.user) + ":" + str(self.service)


class Shop(models.Model):
    name = models.CharField('店铺名称', max_length=32, unique=True)
    create_time = models.DateTimeField('店铺创建时间')
    status = models.BooleanField('店铺状态')
    star = models.IntegerField(verbose_name='店铺星级', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 联接User表

    class Meta:
        db_table = 'Shop'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Type(models.Model):
    name = models.CharField('服务种类名称', max_length=32)

    class Meta:
        db_table = 'Type'

    def __str__(self):
        return self.name

    def __unicode__(self):
        return self.name


class Service(models.Model):
    name = models.CharField('服务名称', max_length=32)
    price = models.DecimalField('服务价格', max_digits=10, decimal_places=2)
    status = models.BooleanField('服务状态')
    img1 = models.CharField('服务图片位置', max_length=255, unique=True, blank=True, null=True)
    img2 = models.CharField('服务图片位置', max_length=255, unique=True, blank=True, null=True)
    intro = models.CharField('服务简介', max_length=255, unique=True, blank=True, null=True)
    sales = models.IntegerField("销量", default=0)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)  # 联接Shop表
    sort = models.ForeignKey('Type', on_delete=models.CASCADE)  # 联接Type表

    class Meta:
        db_table = 'Service'

    def __str__(self):
        return '{0}({1})'.format(self.name, self.sort)

    def __unicode__(self):
        return '{0}({1})'.format(self.name, self.sort)


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
