from django.shortcuts import render


def index(request):
    context = {
        "slogan": "Лучшее предложение"
    }
    return render(request, 'geekshop/index.html', context)


def contact(request):
    context = {

    }
    return render(request, 'geekshop/contact.html', context)
