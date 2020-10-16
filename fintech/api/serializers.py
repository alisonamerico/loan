from rest_framework import serializers
from fintech.api.models import Loan, Payment


class LoanSerializer(serializers.ModelSerializer):

    """
    LoanSerializer - It will be defined which fields
    will be displayed in the Loan view.
    """

    client = serializers.ReadOnlyField(source='client.first_name')

    class Meta:
        model = Loan
        localized_fields = (
            'id', 'client', 'principal', 'interest_rate', 'period',
            'frequency', 'ip_address', 'request_date', 'bank'
        )


class PaymentSerializer(serializers.ModelSerializer):

    """
    LoanSerializer - It will be defined which fields
    will be displayed in the Payment view.
    """

    loan = serializers.ReadOnlyField()

    class Meta:
        model = Payment
        fields = ('id', 'loan', 'payment_date', 'payment_value',)
