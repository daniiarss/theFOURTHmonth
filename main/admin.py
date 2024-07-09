from django.contrib import admin
from main.models import Product
# Register your models here.

class ProductAdmin(admin.ModelAdmin):
    ordering = ['-tittle']
    list_display = ['tittle', 'description', 'price', 'is_active']
    search_fields = ['tittle', 'description']
    list_filter = ['price', 'is_active']
    list_editable = ['price', 'is_active']
    list_per_page = 100
    read_only_fields = ['update']

admin.site.register(Product, ProductAdmin)