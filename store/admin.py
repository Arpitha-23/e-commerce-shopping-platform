from django.contrib import admin
from .models import Category, Product, Order, OrderItem, Wishlist


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'full_name',
        'total_amount',
        'status',
        'created_at'
    )

    list_filter = ('status', 'created_at')

    search_fields = (
        'full_name',
        'email',
        'phone',
        'user__username'
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        'order',
        'product',
        'quantity',
        'price'
    )

    search_fields = (
        'product__name',
        'order__id'
    )


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'product',
        'created_at'
    )

    search_fields = (
        'user__username',
        'product__name'
    )

    list_filter = ('created_at',)