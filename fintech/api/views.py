from fintech.api.serializers import LoanSerializer, PaymentSerializer
from fintech.api.models import Loan, Payment
from rest_framework import viewsets


class LoanViewSet(viewsets.ModelViewSet):

    serializer_class = LoanSerializer
    allowed_methods = ('GET', 'POST')

    def get_queryset(self):
        """
        This view should return a list of all the Loan
        for the currently authenticated user.
        """
        current_client = self.request.user.id
        return Loan.objects.filter(client=current_client)


class PaymentViewSet(viewsets.ModelViewSet):

    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
