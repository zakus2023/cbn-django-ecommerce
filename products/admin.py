from django.contrib import admin

from . models import Product, Category, Order, OrderItem

# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price','slug', 'created_at', 'updated_at', 'status']

@admin.register(Order)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'address','city', 'created_at', 'created_by','email','paid_amount','is_paid','merchant_id', 'status']

@admin.register(OrderItem)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price','quantity']

admin.site.register(Category)


