from django.http import HttpResponse
from django.views import View

from account.models import Service, User
from django.shortcuts import render, redirect


class TestView(View):
    def post(self, request):
        print(request.POST.get("user-name"))
        return HttpResponse("nok")

    def get(self, request):
        return render(request, "test.html")


def print_all_service():
    services = Service.objects.filter()
    for service in services:
        print(service)


def print_all_user():
    users = User.objects.filter()
    for user in users:
        print(user)
