from django.contrib import admin
from basketapp.models import Basket


class BasketAdmin(admin.TabularInline):
    model = Basket
    fields = ('product', 'quantity')
    readonly_fields = ('add_datetime',)
    extra = 0


#admin.site.register(Basket)
