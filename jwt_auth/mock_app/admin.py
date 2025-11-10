from django.contrib import admin

from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'creator', 'amount', 'description')
    list_filter = ('amount',)
    search_fields = ('name', 'creator__email')
    raw_id_fields = ('creator',)
