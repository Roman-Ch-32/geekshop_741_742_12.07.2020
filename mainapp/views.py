import random

from django.core.cache import cache
from django.shortcuts import render, get_object_or_404
from django.views.decorators.cache import never_cache

from basketapp.models import Basket
from geekshop import settings
from mainapp.models import Product, ProductCategory
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render

import json
import os

from django.views.generic import DetailView

from mainapp.models import Product, ProductCategory

MODULE_DIR = os.path.dirname(__file__)
#
# def get_same_products(hot_product):
#     same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
#     return same_products
#
#
# def get_hot_product():
#     products = Product.objects.all()
#     return random.sample(list(products), 1)[0]
#
#
# def products(request, pk=None):
#     title = "каталог"
#     links_menu = ProductCategory.objects.all()
#     hot_product = get_hot_product()
#     same_products = get_same_products(hot_product)
#
#     if pk is not None:
#         if pk == 0:
#             products = Product.objects.all().order_by('price')
#             category = {'name': 'все'}
#         else:
#             category = get_object_or_404(ProductCategory, pk=pk)
#             products = Product.objects.filter(category__pk=pk).order_by('price')
#
#         context = {
#             "title": title,
#             "link_menu": links_menu,
#             "category": category,
#             "related_products": products,
#             "hot_product": hot_product,
#
#         }
#         return render(request, 'mainapp/products.html', context)
#
#     products = Product.objects.all().order_by('price')
#
#     context = {
#         "title": title,
#         "link_menu": links_menu,
#         "related_products": same_products,
#         "products": products,
#         "hot_product": hot_product,
#
#     }
#
#     return render(request, 'mainapp/products.html', context)
#
#
def product(request, pk):
    title = 'продукты'
    links_menu = ProductCategory.objects.all()


    product = get_object_or_404(Product, pk=pk)

    context = {
        'title': title,
        'links_menu': links_menu,
        'product': product,
    }
    return render(request, 'mainapp/product.html', context)


def index(request):
    context = {
        'title': 'Geekshop', }
    return render(request, 'mainapp/index.html', context)

def get_link_category():
    if settings.LOW_CACHE:
        key = 'link_category'
        link_category = cache.get(key)
        if link_category is None:
            link_category = ProductCategory.objects.all()
            cache.set(key,link_category)
        return link_category
    else:
        return ProductCategory.objects.all()

def get_product():
    if settings.LOW_CACHE:
        key = 'link_product'
        link_product = cache.get(key)
        if link_product is None:
            link_product = Product.objects.all().select_related('category')
            cache.set(key, link_product)
        return link_product
    else:
        return Product.objects.all().select_related('category')


def get_product_one(pk):
    if settings.LOW_CACHE:
        key = f'product{pk}'
        product = cache.get(key)
        if product is None:
            product = Product.objects.get(id=pk)
            cache.set(key, product)
        return product
    else:
        return Product.objects.get(id=pk)


@never_cache
def products(request, id_category=None, page=1):

    context = {
        'title': 'Geekshop | Каталог',
    }

    if id_category:
        products = Product.objects.filter(category_id=id_category)
    else:
        products = Product.objects.all().select_related('category')[:3]

    paginator = Paginator(products, per_page=3)

    try:
        products_paginator = paginator.page(page)
    except PageNotAnInteger:
        products_paginator = paginator.page(1)
    except EmptyPage:
        products_paginator = paginator.page(paginator.num_pages)

    context['products'] = products_paginator
    context['categories'] = ProductCategory.objects.all()
    return render(request, 'mainapp/products.html', context)


class ProductDetail(DetailView):
    """
    Контроллер вывода информации о продукте
    """
    model = Product
    template_name = 'mainapp/detail.html'

    # def get_context_data(self, **kwargs):
    #     context = super(ProductDetail, self).get_context_data(**kwargs)
    #     product = self.get_object()
    #     context['product'] = product
    #     return context
    def get_context_data(self, **kwargs):
        context = super(ProductDetail, self).get_context_data(**kwargs)
        # product = self.get_object()
        context['product'] = get_product_one(self.kwargs.get('pk'))
        return context
