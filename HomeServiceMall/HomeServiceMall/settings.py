import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-!i=39zni&$^j%)afnx0h65t6*%^@ucj+67s87$w)9=h8s8$hu6'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

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
# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': "django_mysql",
        'USER': "root",  # 远程数据库账号密码
        'PASSWORD': "123456",
        'HOST': "119.45.125.97",
        'PORT': "3306",  # 远程数据库映射到本地的端口
        'OPTIONS': {'init_command': 'SET default_storage_engine=INNODB;'}
    }
}

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

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
MEDIA_ROOT = os.path.join(BASE_DIR, "static/media")
# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
ALIPAY_PUBLIC = os.path.join(BASE_DIR, 'keys', 'alipay_public.txt')
APP_PUBLIC = os.path.join(BASE_DIR, 'keys', 'app_public.txt')
APP_PRIVATE = os.path.join(BASE_DIR, 'keys', 'app_private.txt')
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.163.com"  # 服务器
EMAIL_PORT = 25  # 一般情况下都为25
EMAIL_HOST_USER = "lets_go2011@163.com"  # 账号
EMAIL_HOST_PASSWORD = "NBMBWKTLJEYOSJLX"  # 密码
EMAIL_USE_TLS = False  # 一般都为False
EMAIL_FROM = "lets_go2011@163.com"  # 邮箱来自
