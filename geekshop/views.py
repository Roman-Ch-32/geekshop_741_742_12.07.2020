from django.shortcuts import render


def index(request):
    return render(request, 'geekshop/index.html')


def contact(request):
    return render(request, 'geekshop/contact.html')
