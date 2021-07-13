from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from utils.util import Util


def about_view(request):
    username, services_sort, is_login = Util.get_basic_info(request)
    return render(request,"about.html",{"username":username,"services_sort":services_sort,"is_login":is_login})


def QA_view(request):
    username, services_sort, is_login = Util.get_basic_info(request)
    return render(request,"Q&A.html",{"username":username,"services_sort":services_sort,"is_login":is_login})

def policy_view(request):
    username, services_sort, is_login = Util.get_basic_info(request)
    return render(request,"privacy_policy.html",{"username":username,"services_sort":services_sort,"is_login":is_login})