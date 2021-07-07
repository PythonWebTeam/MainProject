from django.shortcuts import render

# Create your views here.


def user_info_manage_view(request):
    return render(request,"user_info_manage.html")


def order_info_manage_view(request):
    return render(request,"order_info_manage.html")


def shop_cart_view(request):
    return render(request,"shop_cart.html")


def vendor_info_manage_view(request):
    return render(request,"vendor_info_manage.html")


def shop_info_manage_view(request):
    return render(request,"shop_info_manage.html")


def product_manage_view(request):
    return render(request,"product_manage.html")


def order_manage_view(request):
    return render(request,"order_manage.html")


def service_manage_view(request):
    return render(request,"service_manage.html")


def business_data_view(request):
    return render(request,"business_data.html")