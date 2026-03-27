from django.shortcuts import render,redirect
from django.http import HttpResponse
from dataentry.tasks import celery_test_task
from .forms import RegistrationForm
from django.contrib import messages
def home(request):
    # The template is stored under templates/dataentry/home.html
    return render(request, "home.html")

def celery_test(request):
    celery_test_task.delay()
    return HttpResponse('hi this is celery test')

def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Registration  successful')
            return redirect('register')
        else:
            context = {
                'form': form
            }
            return render(request,'register.html',context)
    else:
        form = RegistrationForm()
        context = {
            'form': form
        }
    return render(request,'register.html',context) 

def login(request):
    return render(request,'login.html')

def logout(request):
    return render(request,'logout.html')