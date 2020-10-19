from fintech.api.serializers import EmprestimoSerializer, PagamentoSerializer
from fintech.api.models import Emprestimo, Pagamento
from rest_framework import viewsets


class EmprestimoViewSet(viewsets.ModelViewSet):

    serializer_class = EmprestimoSerializer
    allowed_methods = ('GET', 'POST')

    def get_queryset(self):
        """
        This view should return a list of all the Emprestimo
        for the currently authenticated user.
        """
        current_client = self.request.user.id
        return Emprestimo.objects.filter(cliente=current_client)


class PagamentoViewSet(viewsets.ModelViewSet):

    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
