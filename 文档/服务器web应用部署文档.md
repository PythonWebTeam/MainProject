[TOC]





















---

# HANDY项目服务器应用部署文档

## 前提：环境准备

1. **服务器操作系统**：Ubuntu 16.04.1 LTS (GNU/Linux 4.15.0-142-generic x86_64)
2. **服务器配置:**1核 2GB 1Mbps  系统盘：50GB高性能云硬盘
3. **公网IP地址**:119.45.125.97

---

## 1.安装 django

### 安装 pip

```
sudo apt install python-pip -y
```

### 使用 pip 安装 django

```
sudo pip install django
```



## 2.创建 HomeServiceMall 应用并启动 Web 服务器

### 创建项目

```
cd /data
sudo django-admin startproject HomeServiceMall
```

### 修改配置文件

修改 /data/HomeServiceMall/HomeServiceMall/settings.py 文件权限为其它人可写

```
sudo chmod 666 /data/HomeServiceMall/HomeServiceMall/settings.py
```

编辑 /data/HomeServiceMall/HomeServiceMall/settings.py

将 `ALLOWED_HOSTS = []` 修改为 `ALLOWED_HOSTS = [*]` ，这样可以允许通过 ip 访问  

### 启动 django 自带的 Web 服务器

```
cd HomeServiceMall
sudo python manage.py runserver 0.0.0.0:8080
```

使用浏览器访问

```
http://119.45.125.97:8080/
```

看到如下页面，表示 django 服务已经部署成功

![image](https://share-10039692.file.myqcloud.com/lab/282e65e37e/image/rdk9vo8wo2/QQ%E5%9B%BE%E7%89%8720171102141913.png)

## 3.创建简单的测试页面

### 关闭 Web 服务器

按 `Ctrl + C` 关闭 Web 服务器

### 创建 views.py

创建文件 /data/HomeServiceMall/HomeServiceMall/views.py ，并修改权限为其它人可写

```
sudo touch /data/HomeServiceMall/HomeServiceMall/views.py
sudo chmod 666 /data/HomeServiceMall/HomeServiceMall/views.py
```

### 添加测试用视图函数

编辑 /data/HomeServiceMall/HomeServiceMall/views.py

添加如下内容：

```python
from django.http.response import HttpResponse
class TestView(View):
    def get(self):
    	return HttpResponse("ok")
```

按 `Ctrl + S` 保存

### 修改 urls.py 文件权限

修改 /data/HomeServiceMall/HomeServiceMall/urls.py 文件权限为其它人可写

```
sudo chmod 666 /data/HomeServiceMall/HomeServiceMall/urls.py
```

### 添加路由配置

编辑 /data/HomeServiceMall/HomeServiceMall/urls.py

将

```
urlpatterns = [
    url(r'^admin/', admin.site.urls),
]
```

修改为

```python
import views
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^test', views.TestView.asView()),
]
```

按 `Ctrl + S` 保存

### 测试 url 访问是否正常

再次启动 Web 服务器

```
sudo python manage.py runserver 0.0.0.0:8080
```

使用浏览器访问下面的 url

```
http://119.45.125.97:8080/test
```

### 关闭 Web 服务器

按 `Ctrl + C` 停止 Web 服务器

## 4.将项目文件移植到HomeServiceMall

使用完整项目文件覆盖原测试项目

配置HomeServiceMall下的settings.py

### 将调试模式DEBUG改为False，并将允许访问的主机改为所有主机ALLOWED_HOSTS=[*]

```python
import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!i=39zni&$^j%)afnx0h65t6*%^@ucj+67s87$w)9=h8s8$hu6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = [*]

```

### 配置APP定义、中间件、Templates模板等

```python
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'account',
    'other',
    "passport",
    "services",
    "shop"
]


SITE_ID = 1
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

]

ROOT_URLCONF = 'HomeServiceMall.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
WSGI_APPLICATION = 'HomeServiceMall.wsgi.application'

LOGIN_URL = "/passport/login/"
OPEN_URLS = ['/passport/login/']

```

### MySQL数据库配置

```python
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "django_mysql",
        'USER': "root",  # 服务器数据库账号密码
        'PASSWORD': "123456",
        'HOST': "119.45.125.97",
        'PORT': "3306", 
        'OPTIONS': {'init_command': 'SET default_storage_engine=INNODB;'}
    }
}

```

### 支付宝配置

```python
# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ALIPAY_PUBLIC = os.path.join(BASE_DIR, 'keys', 'alipay_public.txt')
APP_PUBLIC = os.path.join(BASE_DIR, 'keys', 'app_public.txt')
APP_PRIVATE = os.path.join(BASE_DIR, 'keys', 'app_private.txt')

```

### 邮箱配置

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.163.com"  # 服务器
EMAIL_PORT = 25  # 一般情况下都为25
EMAIL_HOST_USER = "lets_go2011@163.com"  # 账号
EMAIL_HOST_PASSWORD = "NBMBWKTLJEYOSJLX"  # 密码
EMAIL_USE_TLS = False  # 一般都为False
EMAIL_FROM = "lets_go2011@163.com"  # 邮箱来自
```

### 静态文件配置

```python
# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
MEDIA_ROOT = os.path.join(BASE_DIR, "static/media")

```

### 用户认证与国际化等配置

```python
# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

AUTH_USER_MODEL = 'account.User'


# Internationalization

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

```

## 5.部署 uwsgi 和 nginx

### 使用 pip 安装 uwsgi

```
sudo pip install uwsgi
```

### 配置 uwsgi

创建文件 /data/HomeServiceMall/uwsgi.ini ，并修改权限为其它人可写

```
sudo touch /data/HomeServiceMall/uwsgi.ini
sudo chmod 666 /data/HomeServiceMall/uwsgi.ini
```

编辑 /data/HomeServiceMall/uwsgi.ini

输入以下内容，并保存

```
[uwsgi]
chdir = /data/HomeServiceMall
module = HomeServiceMall.wsgi
socket = 127.0.0.1:8080
master = true
vhost = true
no-site = true
workers = 2
reload-mercy = 10     
vacuum = true
max-requests = 1000   
limit-as = 512
buffer-size = 30000
pidfile = /tmp/uwsgi.pid
daemonize = /tmp/uwsgi.log
```

### 启动 uwsgi

```
export PYTHONPATH=/usr/local/lib/python2.7/dist-packages
uwsgi --ini /data/HomeServiceMall/uwsgi.ini
```

### 安装 nginx

```
sudo apt-get install nginx -y
```

### 添加 nginx 配置文件

创建文件 /etc/nginx/sites-enabled/HomeServiceMall.conf ，并修改权限为其它人可写

```
sudo touch /etc/nginx/sites-enabled/HomeServiceMall.conf
sudo chmod 666 /etc/nginx/sites-enabled/HomeServiceMall.conf
```

编辑 /etc/nginx/sites-enabled/HomeServiceMall.conf

输入以下内容，并保存

```java
server {
    listen       80;
    server_name  119.45.125.97;

    charset utf-8;

    location / {
        uwsgi_pass 127.0.0.1:8080;
        include /etc/nginx/uwsgi_params;
        client_max_body_size      10m;
    }

    client_body_timeout  3m;
    send_timeout   3m;
    proxy_send_timeout 3m;
    proxy_read_timeout 3m;
}
```

### 重启 nginx 服务

```
sudo systemctl restart nginx
```

## 6.测试 nginx + uwsgi + django 是否工作正常

### 测试页面是否能够正常访问

使用浏览器通过外网访问部署到服务器的网站主页

```python
http://119.45.125.97/
```

###  测试结果

通过119.45.125.97成功访问到了网站主页

![image-20210717015226949](D:\MainProject\文档\服务器web应用部署文档.assets\image-20210717015226949.png)

整个网站运行正常

![image-20210717020203126](D:\MainProject\文档\服务器web应用部署文档.assets\image-20210717020203126.png)

### 应用部署成功

