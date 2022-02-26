from django.db import transaction

from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect, JsonResponse

from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect

from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from basketapp.models import Basket
from mainapp.mixin import BaseClassContextMixin

from mainapp.models import Product


from ordersapp.forms import OrderItemForm
from ordersapp.models import Order, OrderItem


class OrderListView(ListView, BaseClassContextMixin):
    title = '3аказы'
    model = Order


class OrderCreateView(CreateView, BaseClassContextMixin):
    model = Order
    fields = []
    title = 'Создание заказа'
    success_url = reverse_lazy('orders:list')
    
    def queryset(self):
        return Order.objects.filter(is_active=True)
    
    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST)
        else:
            basket_item = Basket.objects.filter(user=self.request.user)
            if basket_item:
                OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=(basket_item.count()+1),)
                formset = OrderFormSet()
                for num, form in enumerate(formset.forms):
                    form.initial['product'] = basket_item[num].product
                    form.initial['quantity'] = basket_item[num].quantity
                    form.initial['price'] = basket_item[num].product.price
                basket_item.delete()
            else:
                formset = OrderFormSet()
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost == 0:
                self.object.delete()
                
        return super(OrderCreateView, self).form_valid(form)


class OrderUpdateView(UpdateView, BaseClassContextMixin):
    model = Order
    fields = []
    title = 'редактирование заказа'
    success_url = reverse_lazy('orders:list')

    def get_context_data(self, **kwargs):
        context = super(OrderUpdateView, self).get_context_data(**kwargs)

        OrderFormSet = inlineformset_factory(Order, OrderItem, OrderItemForm, extra=1)
        if self.request.POST:
            formset = OrderFormSet(self.request.POST, instance=self.object)
        else:
            formset = OrderFormSet(instance=self.object)
            for form in formset:
                if form.instance.pk:
                    form.initial['price'] = form.instance.product.price
        context['orderitems'] = formset
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        orderitems = context['orderitems']

        with transaction.atomic():
            form.instance.user = self.request.user
            self.object = form.save()
            if orderitems.is_valid():
                orderitems.instance = self.object
                orderitems.save()

            if self.object.get_total_cost == 0:
                self.object.delete()

        return super(OrderUpdateView, self).form_valid(form)


class OrderDeleteView(DeleteView, BaseClassContextMixin):
    model = Order
    title = 'Удаление заказа'
    success_url = reverse_lazy('orders:list')


class OrderDetailView(DetailView, BaseClassContextMixin):
    model = Order
    title = 'Просмотр заказа'


def order_forming_complete(request, pk):
    order = get_object_or_404(Order, pk)
    Order.status = Order.SEND_TO_PROCEEDED
    order.save()
    return HttpResponseRedirect(reverse('orders:list'))


def get_product_price(request, pk):
    if request.is_ajax():
        product = Product.objects.get(id=pk)
        if product:
            return JsonResponse({'price': product.price})

        return JsonResponse({'price': 0})


def payment_result(request):
    # ik_co_id = 51237daa8f2a2d8413000000
    # ik_inv_id = 339800573
    # ik_inv_st = success
    # ik_pm_no = 1
    status = request.GET.get('ik_inv_st')
    if status == 'success':
        order_pk = request.GET.get('ik_pm_no')
        order_item = Order.objects.get(pk=order_pk)
        order_item.status = Order.PAID
        order_item.save()
    return HttpResponseRedirect(reverse('orders:list'))
