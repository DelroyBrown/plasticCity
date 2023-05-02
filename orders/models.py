from django.db import models
from django.conf import settings
from store.models import Customer, Product, Order


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(
        Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_cost(self):
        return self.price * self.quantity


class ShippingOption(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False)

    def __str__(self):
        return self.name
