from django.shortcuts import render
from django.http import HttpResponse
from dataentry.tasks import celery_test_task
from .forms import RegistrationForm
def home(request):
    # The template is stored under templates/dataentry/home.html
    return render(request, "home.html")

def celery_test(request):
    celery_test_task.delay()
    return HttpResponse('hi this is celery test')

def register(request):
    if request.method == "POST":
        return
    else:
        form = RegistrationForm()
        context = {
            'form': form
        }
    return render(request,'register.html',context) 