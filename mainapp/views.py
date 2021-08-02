from django.shortcuts import render, get_object_or_404

from mainapp.models import Product, ProductCategory


def products(request, pk=None):
    
    title = "каталог"

    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
            category = {'name': 'все'}
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products = Product.objects.filter(category__pk=pk).order_by('price')

        context = {
            "title": title,
            "link_menu": links_menu,
            "category": category,
            "related_products": products
        }
        return render(request, 'mainapp/products.html', context)

    same_products = Product.objects.all()[:3]
    products = Product.objects.all().order_by('price')

    context = {
        "title": title,
        "link_menu": links_menu,
        "related_products": same_products,
        "products": products
    }
    
    return render(request, 'mainapp/products.html', context)
