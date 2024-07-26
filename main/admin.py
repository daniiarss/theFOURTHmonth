from django.contrib import admin
from main.models import Product, Review, Size

class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]
    ordering = ['-tittle']
    list_display = ['tittle', 'description', 'price', 'is_active']
    search_fields = ['tittle', 'description']
    list_filter = ['sizes', 'price', 'is_active']
    list_editable = ['price', 'is_active']
    list_per_page = 4
    read_only_fields = ['update']


class ReviewAdmin(admin.ModelAdmin):
    list_display = 'author text stars product product_id'.split()

admin.site.register(Product, ProductAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Size)