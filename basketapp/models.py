from django.db import models

from authapp.models import ShopUser
from geekshop import settings
from mainapp.models import Product


class BasketQuerySet(models.QuerySet):

    def delete(self, *args, **kwargs):
        for item in self:
            item.product.quantity += item.quantity
            item.product.save()
        super(BasketQuerySet, self).delete(*args, **kwargs)


objects = BasketQuerySet.as_manager()


class Basket(models.Model):
    quantity = models.PositiveIntegerField(verbose_name='колличество', default=0)
    add_datetime = models.DateTimeField(verbose_name="время добаввления", auto_now_add=True)
    user = models.ForeignKey(ShopUser, on_delete=models.CASCADE, related_name='basket')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)


    def __str__(self):
        return f'Корзина для  {self.user.username} | Продукт{self.product.name}'


    def get_baskets(self):
        baskets = Basket.objects.filter(user=self.user)
        return baskets

    def sum(self):
        return self.quantity * self.product.price

    def total_sum(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.sum() for basket in baskets)

    def total_quantity(self):
        baskets = Basket.objects.filter(user=self.user)
        return sum(basket.quantity for basket in baskets)

    def delete(self, *args, **kwargs):
        self.product.quantity += self.quantity
        self.product.save()
        super(Basket, self).delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            get_item = self.get_item(int(self.pk))
            self.product.quantity -= (self.quantity - get_item)
        else:
            self.product.quantity -= self.quantity

        self.product.save()
        super(Basket, self).save(*args, **kwargs)

    @staticmethod
    def get_item(pk):
        return Basket.objects.get(pk=pk).quantity
