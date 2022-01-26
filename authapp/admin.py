from django.contrib import admin

from authapp.models import ShopUser
from basketapp.admin import BasketAdmin
from basketapp.models import Basket


@admin.register(ShopUser)
class UserAdmin(admin.ModelAdmin):
    model = Basket
    inlines = (BasketAdmin,)

#admin.site.register(ShopUser)
