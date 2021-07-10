# API开发文档

*基于Django的家政服务平台项目API开发文档*

## 一.管理后台

---

### 登录

方法`POST`  请求地址:`passport/login/`

**描述**

> 登陆接口，使用ajax进行提交请求

**请求头**

| 参数名         | 参数类型 | 描述 |
| -------------- | -------- | ---- |
| `content-type` | `string` | HTML |

**请求参数**

| 参数名          | 参数类型 | 描述                                  |
| --------------- | -------- | ------------------------------------- |
| `user-name`     | `string` | 账号名，3位以上，支持邮箱与手机号登录 |
| `user-password` | `string` | 密码，6-12位                          |

**成功返回**

| 参数名          | 参数类型       | 描述       |
| --------------- | -------------- | ---------- |
| `response_data` | `HttpResponse` | 返回`"ok"` |

**失败返回**

| 参数名         | 参数类型       | 描述             |
| -------------- | -------------- | ---------------- |
| `reponse_data` | `HttpResponse` | 登录失败提示信息 |

**说明/示例**

​	登录成功后，session保留了登录状态

---

### 注册

方法`POST`  请求地址:`passport/register/` 

**描述**

> 注册接口，使用ajax进行提交请求

**请求头**

| 参数名         | 参数类型 | 描述 |
| -------------- | -------- | ---- |
| `content-type` | `string` | HTML |

**请求参数**

| 参数名          | 参数类型 | 描述                                  |
| --------------- | -------- | ------------------------------------- |
| `data`          | `dict`   | 包含用户注册时所有信息                |
| `user-name`     | `string` | 账号名，3位以上，支持邮箱与手机号登录 |
| `user-password` | `string` | 密码，6-12位                          |
| `phone-number`  | `string` | 手机号码，11位                        |
| `user-email`    | `string` | 邮箱，格式为邮箱格式                  |
| `prov`          | `int`    | 省份代码                              |
| `city`          | `int`    | 市代码                                |
| `county`        | `int`    | 县代码                                |
| `address`       | `string` | 详细地址                              |

**成功返回**

| 参数名          | 参数类型       | 描述                  |
| --------------- | -------------- | --------------------- |
| `response_data` | `HttpResponse` | 注册成功，返回 `"ok"` |

**失败返回**

| 参数名            | 参数类型       | 描述             |
| ----------------- | -------------- | ---------------- |
| ``response_data`` | `HttpResponse` | 注册失败提示信息 |

**说明/示例**

---

## 2.服务列表

---

### 获取服务列表页面

方法`GET`  请求地址:`services/?search={{key}}` 

**描述**

> 获取服务列表页面，通过关键字`key`搜索

**请求头**

| 参数名         | 参数类型 | 描述 |
| -------------- | -------- | ---- |
| `content-type` | `string` | HTML |

**请求参数**

| 参数名 | 参数类型 | 描述       |
| ------ | -------- | ---------- |
| `name` | `string` | 服务种类名 |

**成功返回**

| 参数名         | 参数类型    | 描述                      |
| -------------- | ----------- | ------------------------- |
| `services`     | `Service[]` | 搜索结果`Service`对象列表 |
| `services_num` | `int`       | 服务总个数                |
| `key`          | `string`    | 搜索关键字                |

```
增加搜索关键字
```

**失败返回**

| 参数名 | 参数类型       | 描述                  |
| ------ | -------------- | --------------------- |
|        | `HttpResponse` | 返回`"404 Not Found"` |

**说明/示例**

---

`Service`对象所含参数如下

```python
    name = models.CharField('服务名称', max_length=32)
    price = models.DecimalField('服务价格', max_digits=10, decimal_places=2)
    status = models.BooleanField('服务状态')
    img1 = models.CharField('服务图片位置', max_length=255, unique=True, blank=True, null=True)
    img2 = models.CharField('服务图片位置', max_length=255, unique=True, blank=True, null=True)
    intro = models.CharField('服务简介', max_length=255, unique=True, blank=True, null=True)
    sales = models.IntegerField("销量", default=0)
    shop = models.ForeignKey('Shop', on_delete=models.CASCADE)  # 联接Shop表
    sort = models.ForeignKey('Type', on_delete=models.CASCADE)  # 联接Type表
```

获取 商品种类名 使用`services.下标.sort.name`

HTML用`for`循环显示图片

---

## 3.店铺

### 获取服务详情页面

方法`GET` 请求地址:`shop/service/?se_id={{service.id}}}`

**描述**

> 获取服务详情页面

**请求头**

| 参数名         | 参数类型 | 描述 |
| -------------- | -------- | ---- |
| `content-type` | `string` | HTML |

**请求参数**

| 参数名  | 参数类型 | 描述     |
| ------- | -------- | -------- |
| `se_id` | `int`    | 服务id号 |

**成功返回**

| 参数名     | 参数类型  | 描述                             |
| ---------- | --------- | -------------------------------- |
| `service`  | `Service` | `Service`对象                    |
| `is_login` | `boolean` | 判断是否登录，为`True`时为登录态 |

```
点击购买时未登录跳转登录页面
```

**失败返回**

| 参数名 | 参数类型       | 描述                  |
| ------ | -------------- | --------------------- |
|        | `HttpResponse` | 返回`"404 Not Found"` |

**说明/示例**

---

### 获取订单支付页面

方法`GET` 请求地址:`shop/service/pay/?se_id={{service.id}}`

```
传递数组
```

**描述**

> 获取订单支付页面，当未登录时会被重定向至登录页面

**请求头**

| 参数名         | 参数类型 | 描述 |
| -------------- | -------- | ---- |
| `content-type` | `string` | HTML |

**请求参数**

| 参数名  | 参数类型 | 描述     |
| ------- | -------- | -------- |
| `se_id` | `int`    | 服务id号 |

**成功返回**

| 参数名    | 参数类型  | 描述          |
| --------- | --------- | ------------- |
| `service` | `Service` | `Service`对象 |

**失败返回**

| 参数名 | 参数类型       | 描述                  |
| ------ | -------------- | --------------------- |
|        | `HttpResponse` | 返回`"404 Not Found"` |

**说明/示例**

