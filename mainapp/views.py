from django.shortcuts import render

from mainapp.models import Product, ProductCategory


def index(request):
    
    title = "каталог"

    links_menu = ProductCategory.objects.all()

    products = Product.objects.all()[:3]

    context = {
        "title": title,
        "link_menu": links_menu,
        "related_products": products
    }
    
    return render(request, 'mainapp/products.html', context)
