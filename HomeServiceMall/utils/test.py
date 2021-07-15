from django.http import HttpResponse

from account.models import Service


def test_view(request):
    services = Service.objects.all()
    for service in services:
        path = service.img1
        print(path)
    return HttpResponse("ok")
