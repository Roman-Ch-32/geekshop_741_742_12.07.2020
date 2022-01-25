from django.db import models

from geekshop import settings
from mainapp.models import Product


class Basket(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(verbose_name='колличество', default=0)
    add_datetime = models.DateTimeField(verbose_name="время добаввления", auto_now_add=True)

    @property
    def total_quantity(self):
        items = Basket.objects.filter(user=self.user)
        total_quantity = sum(list(map(lambda x: x.quantity, items)))
        return total_quantity

    @property
    def product_cost(self):
        return self.product.price * self.quantity

    @property
    def total_cost(self):
        items = Basket.objects.filter(user=self.user)
        total_cost = sum(list(map(lambda x: x.product_cost, items)))
        return total_cost
