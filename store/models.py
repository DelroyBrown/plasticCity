from django.db import models
from django.apps import apps
from django.urls import reverse
from decimal import Decimal
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinLengthValidator
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(max_length=100, blank=False,
                            null=False, unique=True)

    def get_absolute_url(self):
        return reverse('store:product_list_by_category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    slug = models.SlugField(max_length=100, unique=True,
                            blank=False, null=False)
    description = models.TextField(
        max_length=500, default='', blank=True, null=True)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, blank=False, null=False)
    image = models.ImageField(upload_to='media/product_images/')
    category = models.ForeignKey(
        Category, related_name='products', on_delete=models.CASCADE)
    stock = models.PositiveIntegerField()
    shipping_options = models.ManyToManyField(
        'orders.ShippingOption', related_name='products', through='ProductShippingOption')
    material = models.CharField(max_length=100, blank=True, null=True)
    print_time = models.DecimalField(
        max_digits=10, decimal_places=0, blank=True, null=True)
    infill = models.PositiveIntegerField(blank=True, null=True)
    printer_type = models.CharField(max_length=100, blank=True, null=True)
    detail_view_link = models.CharField(max_length=100, blank=False, null=False,
                                        default="'store:product_detail' category_slug=product.category.slug product_slug=product.slug")

    id_tab = models.CharField(
        max_length=20, blank=True, null=True, default='tab-')

    def get_absolute_url(self):
        return reverse('store:product_detail', args=[self.id, self.slug])

    def __str__(self):
        return self.name

    def get_shipping_options(self):
        ShippingOption = apps.get_model('orders', 'ShippingOption')
        return ShippingOption.objects.filter(products=self)


class ProductShippingOption(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    shipping_option = models.ForeignKey(
        'orders.ShippingOption', on_delete=models.CASCADE)


class Customer(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    postal_code = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=255, default='')
    email = models.EmailField(max_length=200, default='')
    address = models.CharField(max_length=255, default='')
    city = models.CharField(max_length=100, default='')
    postal_code = models.CharField(
        max_length=12, default='', validators=[MinLengthValidator(4)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00)
    shipping_option = models.ForeignKey(
        'orders.ShippingOption', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-created_at']

    def get_total_cost(self):
        total_cost = Decimal(self.total_price) + \
            Decimal(self.shipping_option.price)
        return total_cost

    def __str__(self):
        return f'Order {self.id}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return str(self.id)


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def __str__(self):
        return f"{self.user.username}'s Wishlist"


def create_customer(sender, instance, created, **kwargs):
    if created:
        Customer.objects.create(user=instance)


post_save.connect(create_customer, sender=User)
