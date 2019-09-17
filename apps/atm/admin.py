from django.contrib import admin
from apps.atm.models import Deposit, Transaction, TransactionDetail


class DepositAdmin(admin.ModelAdmin):
    list_display = ('currency', 'value', 'quantity', 'created')
    list_filter = ('currency', 'value')
    ordering = ('currency', '-value')


class TransactionDetailInline(admin.TabularInline):
    model = TransactionDetail
    fields = ('value', 'quantity', 'created')
    readonly_fields = ('value', 'quantity', 'created')

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


class TransactionAdmin(admin.ModelAdmin):
    list_display = ('transaction_type', 'currency', 'created')
    list_filter = ('transaction_type', 'currency')
    ordering = ('-id',)
    inlines = [TransactionDetailInline]


admin.site.register(Deposit, DepositAdmin)
admin.site.register(Transaction, TransactionAdmin)
