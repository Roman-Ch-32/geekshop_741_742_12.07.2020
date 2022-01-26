from django.db import models

# Create your models here.


class ProductCategory(models.Model):
    href = models.TextField(blank=True, verbose_name="ссылка")
    name = models.CharField(verbose_name="имя", max_length=128, unique=True)
    description = models.TextField(verbose_name="описание", max_length=750, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории товаров'


class Product(models.Model):
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name="категория товара")
    name = models.CharField(verbose_name="имя", max_length=128, unique=True)
    short_description = models.CharField(verbose_name="короткое описание", max_length=256, blank=True)
    description = models.TextField(verbose_name="описание", max_length=1000, blank=True)
    img = models.ImageField(upload_to="products_img", blank=True, verbose_name="картинка")
    price = models.DecimalField(verbose_name="цена", max_digits=10, decimal_places=2, default=0)
    quantity = models.PositiveIntegerField(verbose_name='колличество', default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} | {self.category}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
