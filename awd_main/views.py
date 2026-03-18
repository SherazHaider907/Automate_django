from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    # The template is stored under templates/dataentry/home.html
    return render(request, "dataentry/home.html")

def celery_test(request):
    return HttpResponse('hi this is celery test')