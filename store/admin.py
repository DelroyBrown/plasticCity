from django.contrib import admin
from .models import (Category,
                     Product,
                     Customer,
                     Order,
                     OrderItem,
                     Wishlist)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'category']
    list_editable = ['price', 'stock']
    prepopulated_fields = {'slug': ('name',)}


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'city', 'postal_code']


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'created_at', 'updated_at', 'paid', 'shipping_option']
    list_filter = ['paid', 'created_at', 'updated_at', 'shipping_option']
    inlines = [OrderItemInline]


class WishlistAdmin(admin.ModelAdmin):
    list_display = ('user', 'products_count')

    def products_count(self, obj):
        return obj.products.count()

    products_count.short_description = 'Number of Products'


admin.site.register(Order, OrderAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category, CategoryAdmin)
