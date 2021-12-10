from django.contrib import admin

from .models import Bill


class BillAdmin(admin.ModelAdmin):
    list_filter = ('company_name', 'client')
    fields = ('client', 'company_name', 'nit', 'code', 'products')
    list_display = (
        'id',
        'client',
        'company_name',
        'nit',
        'code',
    )
    search_fields = ('nit',)


admin.site.register(Bill, BillAdmin)
