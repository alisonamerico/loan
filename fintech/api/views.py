from fintech.api.serializers import EmprestimoSerializer, PagamentoSerializer
from fintech.api.models import Emprestimo, Pagamento
from rest_framework import viewsets
# from ipware.ip import get_client_ip


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

    # def get_client_ip(request):
    #     """
    #     Function to get the client's IP address
    #     """
    #     x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    #     if x_forwarded_for:
    #         ip_address = x_forwarded_for.split(',')[0]
    #     else:
    #         ip_address = request.META.get('REMOTE_ADDR')
    #     return ip_address

    # def get_ip(self, reques):
    #     request = HttpRequest()
    #     client_ip, is_routable = get_client_ip(request)
    #     if client_ip is None:


class PagamentoViewSet(viewsets.ModelViewSet):

    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
