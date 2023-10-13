from django.contrib import admin

from purchases.models.order import Order
from purchases.models.purchase import Purchase

# Register your models here.

admin.site.register(Order)
admin.site.register(Purchase)
