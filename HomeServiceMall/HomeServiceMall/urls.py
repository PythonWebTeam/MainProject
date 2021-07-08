from django.contrib import admin
from django.urls import path, include
from . import views
from account import views as account_views
from other import views as other_views
from passport import views as passport_views
from services import views as services_views
from shop import views as shop_views

# users urls
from .views import test_view

users_patterns = [
    path("user_info_manage/", account_views.user_info_manage_view),
    path("order_info_manage/", account_views.order_info_manage_view),
    path("shop_cart/", account_views.shop_cart_view),
]
# vendors urls
vendors_patterns = [
    path("vendor_info_manage/", account_views.vendor_info_manage_view),
    path("shop_info_manage/", account_views.shop_info_manage_view),
    path("product_manage/", account_views.product_manage_view),
    path("order_manage/", account_views.order_manage_view),
    path("service_manage/", account_views.service_manage_view),
    path("business_data/", account_views.business_data_view),
]
# account urls
account_patterns = [
    path("users/", include(users_patterns)),
    path("vendors/", include(vendors_patterns)),
]

# passport urls
passport_patterns = [
    path("login/", passport_views.Login_view.as_view()),
    path("register/", passport_views.register_view),
    path("retrieve/", passport_views.retrieve_view),
]
# services urls
services_patterns = [
    path("<str:service_class>/", services_views.services_class_view),
]
# shop urls
shop_patterns = [
    path("", shop_views.shop_view),
    path("<str:service>/", shop_views.service_view),
    path("<str:service>/pay", shop_views.pay_view),
]
# other urls
other_patterns = [
    path("about/", other_views.about_view),
    path("Q&A/", other_views.QA_view),
]
# main urls
urlpatterns = [
    path("", views.Home_view.as_view()),
    path("account/", include(account_patterns)),
    path("passport/", include(passport_patterns)),
    path("shop/", include(shop_patterns)),
    path("services/", include(services_patterns)),
    path("other/", include(other_patterns)),
    path("admin/", admin.site.urls),
    path("test/",test_view)
]
