from django.contrib import admin
from django.urls import path, include

from utils import send_email
from utils.data import alipay_index
from . import views
from account import views as account_views
from other import views as other_views
from passport import views as passport_views
from services import views as services_views
from shop import views as shop_views

# users urls
users_patterns = [
    path("user_info_manage/", account_views.UserInfoManageView.as_view()),
    path("order_info_manage/", account_views.order_info_manage_view),
    path("shop_cart/", account_views.ShopCartView.as_view()),
]

# vendors urls
vendors_patterns = [
    path("vendor_info_manage/", account_views.VendorInfoManageView.as_view()),
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
    path("change_psw/",account_views.ChangePasswordView.as_view()),
]

# passport urls
passport_patterns = [
    path("login/", passport_views.LoginView.as_view()),
    path("register/", passport_views.RegisterView.as_view()),
    path("retrieve/", passport_views.RetrieveView.as_view()),
    path("email_auth/", send_email.SendEmailView.as_view()),
    path("logout/",passport_views.LogoutView.as_view())
]

# shop urls
shop_patterns = [
    path("", shop_views.ShopView.as_view()),
    path("service/", shop_views.ServiceView.as_view()),
    path("service/pay/", shop_views.PayView.as_view()),
    path("service/pay/alipay/",alipay_index)
]

# other urls
other_patterns = [
    path("about/", other_views.about_view),
    path("Q&A/", other_views.QA_view),
    path("privacy_policy/",other_views.policy_view),
]

# main urls
urlpatterns = [
    path("", views.HomeView.as_view()),
    path("account/", include(account_patterns)),
    path("passport/", include(passport_patterns)),
    path("shop/", include(shop_patterns)),
    path("services/", services_views.ServicesClassView.as_view()),
    path("other/", include(other_patterns)),
    path("admin/", admin.site.urls),
]
