from django.contrib import admin
from .models import OrderItem, ShippingOption

class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'product', 'price', 'quantity']

admin.site.register(OrderItem, OrderItemAdmin)
admin.site.register(ShippingOption)
