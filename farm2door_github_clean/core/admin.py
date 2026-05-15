from django.contrib import admin
from .models import Product, Order, OrderItem, Profile


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'farmer', 'price', 'stock')
    list_filter = ('farmer',)
    search_fields = ('name', 'farmer__username')
    fields = ('farmer', 'name', 'price', 'stock', 'image')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'total', 'payment_method', 'payment_status', 'created_at')
    list_filter = ('payment_method', 'payment_status', 'created_at')
    search_fields = ('customer__username',)


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    search_fields = ('product__name', 'order__customer__username')


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_type')
    list_filter = ('user_type',)
    search_fields = ('user__username',)


admin.site.site_header = 'Farm2Door Administration'
admin.site.site_title = 'Farm2Door Admin'
admin.site.index_title = 'Gestion Farm2Door'
