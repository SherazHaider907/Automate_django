from django.shortcuts import render
from django.http import HttpResponse
from dataentry.tasks import celery_test_task
def home(request):
    # The template is stored under templates/dataentry/home.html
    return render(request, "dataentry/home.html")

def celery_test(request):
    celery_test_task.delay()
    return HttpResponse('hi this is celery test')