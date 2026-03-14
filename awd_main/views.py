from django.shortcuts import render


def home(request):
    # The template is stored under templates/dataentry/home.html
    return render(request, "dataentry/home.html")