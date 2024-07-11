from django.contrib import admin

from . models import Product, Category

# Register your models here.

@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'price','slug', 'created_at', 'updated_at', 'status']

admin.site.register(Category)


