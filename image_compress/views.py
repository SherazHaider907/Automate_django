from django.shortcuts import render

# Create your views here.
def compress(request):
    return render(request, "image_compress/compress.html")