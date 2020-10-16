from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


class Loan(models.Model):
    """
    This class contains the representation of the fields in the Loan table.
    """
    FREQUENCY = [
        ('ANNUALLY-1', 'Annually'),
        ('SEMI-ANNUALLY-2', 'Semi-Annually'),
        ('QUARTERLY-4', 'Quarterly'),
        ('BI-MONTHLY-6', 'Bi-Monthly'),
        ('MONTHLY-12', 'Monthly'),
        ('BI-WEEKLY-24', 'Bi-Weekly'),
    ]

    client = models.OneToOneField(
        get_user_model(), verbose_name='Client', on_delete=models.CASCADE
    )
    principal = models.DecimalField(
        verbose_name='Principal', max_digits=8, decimal_places=2
    )
    interest_rate = models.FloatField(
        verbose_name='Interest Rate', default=0, validators=[MinValueValidator(0)]
    )
    period = models.IntegerField(verbose_name='Period')
    frequency = models.CharField(
        verbose_name='Frequency of Payment', max_length=15, choices=FREQUENCY, default='MONTHLY-12'
    )
    ip_address = models.GenericIPAddressField(verbose_name='IP Address', protocol='IPV4')
    request_date = models.DateTimeField(verbose_name='Request Date', auto_now_add=True)
    bank = models.CharField(verbose_name='Bank', max_length=50)

    class Meta:
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'
        ordering = ["request_date"]

    def __str__(self):
        """A string representation of the model."""
        return f'{self.client}, {self.principal}, {self.interest_rate}, {self.period}, \
        {self.frequency}, {self.ip_address}, {self.request_date}, {self.bank}'

    def calculate_amortization_amount(principal, interest_rate, period):
        """
        Calculates Amortization Amount per period
        :param principal: Principal amount
        :param interest_rate: Interest rate per period
        :param period: Total number of periods
        :return: Amortization amount per period
        """
        x = (1 + interest_rate) ** period
        return principal * (interest_rate * x) / (x - 1)

    def amortization_schedule(principal, interest_rate, period, calculate_amortization_amount):
        """
        Generates amortization schedule
        :param principal: Principal amount
        :param interest_rate: Interest rate per period
        :param period: Total number of periods
        :return: Rows containing period, interest, principal, balance, etc
        """
        amortization_amount = calculate_amortization_amount
        number = 1
        balance = principal
        while number <= period:
            interest = balance * interest_rate
            principal = amortization_amount - interest
            balance = balance - principal
            yield number, amortization_amount, interest, principal, balance if balance > 0 else 0
            number += 1

    def get_address_client_ip(request):
        """
        Function to get the client's IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip_address = x_forwarded_for.split(',')[0]
        else:
            ip_address = request.META.get('REMOTE_ADDR')
        return ip_address


class Payment(models.Model):
    """
    This class contains the representation of the fields in the Payment table.
    """
    loan_id = models.ForeignKey(
        'api.Loan', related_name='payment_loan', on_delete=models.DO_NOTHING,
        null=True, default=None, blank=True
    )
    payment_date = models.DateTimeField(verbose_name='Payment Date', auto_now_add=True)
    payment_value = models.DecimalField(
        verbose_name='Payment Value', max_digits=8, decimal_places=2
    )

    class Meta:
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'

    def __str__(self):
        """A string representation of the model."""
        return f'{self.loan_id}, {self.payment_date}, {self.payment_value}'
