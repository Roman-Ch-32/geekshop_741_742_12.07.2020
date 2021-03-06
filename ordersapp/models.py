from django.conf import settings
from django.db import models

from mainapp.models import Product


class Order(models.Model):

    FORMING = 'FRM'
    SEND_TO_PROCEEDED = 'STP'
    PAID = 'PD'
    PROCEEDED = 'PRD'
    READY = 'RDY'
    CANCEL = 'CNC'

    ORDER_STATUS_CHOICES = (
        (FORMING, 'формируется'),
        (SEND_TO_PROCEEDED, 'отправлен в обработку'),
        (PAID, 'оплачено'),
        (READY, 'готово к выдаче'),
        (CANCEL, 'отмена заказа'),
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    create = models.DateTimeField(verbose_name='создан', auto_now_add=True)
    apdate = models.DateTimeField(verbose_name='обновлён', auto_now_add=True)
    status = models.CharField(verbose_name='статус', choices=ORDER_STATUS_CHOICES, max_length=3, default=FORMING)
    is_active = models.BooleanField(verbose_name='активный', default=True)

    def __str__(self):
        return f'текущий заказ {self.pk}'

    def get_total_quatity(self):
        items = self.orderitems.select_related('product')
        return sum(list(map(lambda x: x.quantity, items)))

    def get_total_cost(self):
        items = self.orderitems.select_related('product')
        return sum(list(map(lambda x: x.get_product_cost(), items)))

    def get_summary(self):
        items = self.orderitems.select_related()
        return {
            'total_cost': sum(list(map(lambda x: x.quantity * x.product.price, items))),
            'total_quantity': sum(list(map(lambda x: x.quantity, items)))
        }

    def get_items(self):
        pass

    def delete(self, using=None, keep_parents=False):
        for item in self.orderitems.select_related('product'):
            item.product.quantity += item.quantity
            item.save()
        self.is_active = False
        self.save()


class OrderItem(models.Model):
    order = models.ForeignKey(Order, verbose_name='заказ', related_name='orderitems', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, verbose_name='продукты', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='количество', default=0)

    def get_product_cost(self):
        return self.product.price * self.quantity
