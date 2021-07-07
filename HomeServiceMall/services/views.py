from django.shortcuts import render

# Create your views here.
def services_class_view(request):
    return render(request,"services_class.html")