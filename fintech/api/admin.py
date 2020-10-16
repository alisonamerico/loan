from django.contrib import admin
from fintech.api.models import Loan, Payment


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    """
    It will be defined which fields will be displayed
    in the Loan view in the Admin
    """
    list_display = ('client', 'principal', 'interest_rate', 'period',
                    'frequency', 'ip_address', 'request_date', 'bank',)
    search_fields = ['client', 'ip_address', 'request_date', 'bank']
    ordering = ('-client',)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """
    It will be defined which fields will be displayed
    in the Payment view in the Admin
    """
    list_display = ('loan_id', 'payment_date', 'payment_value')
    search_fields = ['loan_id', 'payment_date', 'payment_value']
    ordering = ('-payment_date',)
