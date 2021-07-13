from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def about_view(request):
    return render(request,"about.html")


def QA_view(request):
    return render(request,"Q&A.html")

def policy_view(request):
    return render(request,"privacy_policy.html")