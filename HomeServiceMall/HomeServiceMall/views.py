from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.db import connection

def home_view(request):

    return render(request, "home.html")
