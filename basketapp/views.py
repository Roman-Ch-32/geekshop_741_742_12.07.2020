from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.db import connection
from django.db.models import F, Q

from basketapp.models import Basket
from mainapp.models import Product

from django.contrib.auth.decorators import login_required

from django.template.loader import render_to_string
from django.http import JsonResponse


@login_required
def basket_add(request, id):
    user_select = request.user
    product = Product.objects.get(id=id)
    baskets = Basket.objects.filter(user=user_select, product=product)
    test = get_object_or_404(Product, pk=500)
    if baskets:
        basket = baskets.first()
        basket.quantity = F('quantity')+1
        basket.save()
        update_queries = list(filter(lambda x: 'UPDATE' in x['sql'], connection.queries))
        print(f'basket_add {update_queries} ')
    else:
        Basket.objects.create(user=user_select, product=product, quantity=1)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_remove(request, pk):
    basket_record = get_object_or_404(Basket, pk=pk)
    basket_record.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def basket_edit(request, id_basket, quantity):
    if request.is_ajax():
        basket = Basket.objects.get(id=id_basket)
        if quantity > 0:
            basket.quantity = quantity
            basket.save()
        else:
            basket.delete()

        baskets = Basket.objects.filter(user=request.user)
        context = {'baskets': baskets}
        result = render_to_string('basketapp/basket.html', context)
        test = JsonResponse({'result': result})
        return test
