from django.contrib import admin

from .models import Product


class ProductAdmin(admin.ModelAdmin):
    list_filter = ('name', 'description')
    fields = ('name', 'description')
    list_display = (
        'id',
        'name',
        'description',
    )
    search_fields = ('name', 'description')


admin.site.register(Product, ProductAdmin)
