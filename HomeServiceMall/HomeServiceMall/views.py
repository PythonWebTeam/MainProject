from django.http.response import  HttpResponse
from django.shortcuts import render
def test(request):
    return HttpResponse("content changed")