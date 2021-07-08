from django.db import models

# Create your models here.

"""
创建学生信息表模型
"""

from django.db import models


class Cart(models.Model):
    service = models.ForeignKey('Service', on_delete=models.CASCADE)  # 联接Service表
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # 联接User表

    class Meta:
        db_table = 'Cart'

    def __str__(self):
        return "服务:" + str(self.service) + " 用户:" + str(self.user.username)


class User(models.Model):
    username = models.CharField('用户名', max_length=32, unique=True)
    password = models.CharField('密码', max_length=32)
    email = models.EmailField('用户邮箱', unique=True, blank=True, null=True)
    phone = models.CharField('用户电话', max_length=32, unique=True, blank=True, null=True)
    ban = models.BooleanField('用户账号状态')
    country = models.CharField('国家', max_length=32)
    province = models.CharField('省份', max_length=32)
    district = models.CharField('区县', max_length=32)
    details = models.CharField('详细地址', max_length=255)
    role = models.ForeignKey('Role', on_delete=models.CASCADE)  # 联接Role表

    def __str__(self):
       
        return "id:{} 姓名:{} 密码:{} 邮箱:{} 电话:{} 状态:{} 国家:{} 省份:{} 区县:{} 详细地址:{} 类别:{}".format( \
            self.id, self.username, self.password, self.email, self.phone, \
            self.ban, self.country, self.province, self.district, self.details, self.role.permission
        )

    def get_cart(self):
        return Cart.objects.filter(user_id=self.id)

    class Meta:
        db_table = 'User'


class Role(models.Model):
    permission = models.CharField('用户权限', max_length=32)

    class Meta:
        db_table = 'Role'


class Order(models.Model):
    service = models.ForeignKey('Service', null=True, blank=True, on_delete=models.SET_NULL)  # 联接Service表
    user = models.ForeignKey('User', null=True, blank=True, on_delete=models.SET_NULL)  # 联接User表
    create_time = models.DateTimeField('订单创建时间')
    start_time = models.DateTimeField('订单开始时间')
    end_time = models.DateTimeField('订单结束时间')
    pay_status = models.BooleanField('订单支付状态')

    class Meta:
        db_table = 'Order'


class Shop(models.Model):
    name = models.CharField('店铺名称', max_length=32, unique=True)
    create_time = models.DateTimeField('店铺创建时间')
    status = models.BooleanField('店铺状态')
    user = models.ForeignKey('User', on_delete=models.CASCADE)  # 联接User表

    class Meta:
        db_table = 'Shop'


class Type(models.Model):
    name = models.CharField('服务种类名称', max_length=32)

    class Meta:
        db_table = 'Type'


class Service(models.Model):
    name = models.CharField('服务名称', max_length=32)
    price = models.DecimalField('服务价格', max_digits=10, decimal_places=2)
    status = models.BooleanField('服务状态')
    img = models.CharField('服务图片位置', max_length=255, unique=True, blank=True, null=True)
    intro = models.CharField('服务简介', max_length=255, unique=True, blank=True, null=True)
    sales = models.IntegerField("销量", default=0)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)  # 联接Shop表
    sort = models.ForeignKey('Type', on_delete=models.CASCADE)  # 联接Type表

    def __str__(self):
        return "id:{} 姓名:{} 价格:{} 状态:{} 简介:{} 所属店铺:{} 类别:{} 销量:{} imgurl:{}".format( \
            self.id, self.name, self.price, self.status, self.intro, self.shop.name, self.sort.name, self.sales,self.img)

    class Meta:
        db_table = 'Service'
