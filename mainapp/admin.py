from django.contrib import admin

from mainapp.models import ProductCategory
from mainapp.models import Product

admin.site.register(ProductCategory)
admin.site.register(Product)
