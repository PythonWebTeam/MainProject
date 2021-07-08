from account.models import Service, User
from django.shortcuts import render, redirect


def test_view(request):
    print_all_service()
    return render(request, "test.html")


def print_all_service():
    services = Service.objects.filter()
    for service in services:
        print(service)


def print_all_user():
    users = User.objects.filter()
    for user in users:
        print(user)
