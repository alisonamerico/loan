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
        return Emprestimo.objects.filter(client=current_client)

    def calcula_taxa_juros_em_percentual(taxa_juros):
        """
        Calcula a taxa de juros em percentual. Ex. 1%
        :param taxa_juros_percentual: Valor da taxa de juros em percentual esperada.
        :param taxa_juros: Taxa de Juros por periodo
        :return taxa_juros_percentual:  Retorna valor da taxa de juros em percentual.
        """
        taxa_juros_percentual = taxa_juros / 100
        return taxa_juros_percentual

    def calcula_valor_parcela(valor_nominal, calcula_taxa_juros_em_percentual, periodo):
        """
        Calcula valor da parcela a ser paga
        :param valor_nominal: Valor atual do empréstimo
        :param taxa_juros: Taxa de Juros por periodo
        :param periodo: Número de meses
        :return valor_parcela:  Retorna valor da parcela a ser paga por mês
        """
        valor_parcela = (valor_nominal * calcula_taxa_juros_em_percentual) / \
            (1 - (1 / (1 + calcula_taxa_juros_em_percentual) ** periodo))
        return valor_parcela

    def calcula_valor_juros_em_reais(valor_nominal, calcula_taxa_juros_em_percentual):
        """
        Calcula valor dos juros a ser pago em reais.
        :param valor_nominal: Valor total que resta pagar em cada periodo.
        :param taxa_juros: Taxa de Juros por periodo
        :return valor_juros_em_reais:  Retorna o valor do juros em reais.
        """
        valor_juros_em_reais = valor_nominal * calcula_taxa_juros_em_percentual
        return valor_juros_em_reais

    def calcula_valor_amortizacao(calcula_valor_parcela, calcula_valor_juros_em_reais):
        """
        Calcula valor da amortização
        :param calcula_valor_parcela: Função que calcula o valor da parcela.
        :param calcula_valor_juros_em_reais: Função que calcula valor juros em reais.
        :return amortizacao:  Retorna o valor do amortização.
        """
        amortizacao = calcula_valor_parcela - calcula_valor_juros_em_reais
        return amortizacao

    def calcula_saldo_devedor(valor_nominal, calcula_valor_amortizacao):
        """
        Calcula valor do saldo devedor.
        :param valor_nominal: Valor total que resta pagar em cada periodo.
        :param calcula_valor_amortizacao: Função que calcula o valor da amortização.
        :return saldo_devedor:  Retorna o valor do do saldo devedor.
        """
        saldo_devedor = valor_nominal - calcula_valor_amortizacao
        return saldo_devedor

    # def cronograma_de_amortizacao(valor_nominal, calcula_valor_amortizacao,
    #                               calcula_saldo_devedor, periodo
    #                               ):
    #     """
    #     Função que gera uma lista com os valores de:
    #     periodo (meses) | valor_parcela | amortizacao | valor_juros_em_reais | saldo_devedor
    #     :param valor_nominal: Valor total que resta pagar ou saldo devedor em cada periodo.
    #     :param calcula_valor_amortizacao: Função que calcula o valor da amortização.
    #     :param taxa_juros_percentual: Valor da taxa de juros em percentual esperada.
    #     :param periodo: Número de meses
    #     :return Retorna periodo (meses), valor_parcela, amortizacao, valor_juros_em_reais, saldo_devedor
    #     enquanto o número de parcelas a serem pagas forem menores que o período acordado para ser pago.
    #     """
    #     numero_parcelas = 1
    #     valor_amortizacao = calcula_valor_amortizacao
    #     saldo_devedor = calcula_saldo_devedor
    #     while numero_parcelas <= periodo:  # <-- parei aqui
    #         # valor_nominal = saldo_devedor
    #         # yield numero_parcelas, valor_amortizacao, valor_nominal, saldo_devedor \
    #         #     if saldo_devedor > 0 else 0
    #         # numero_parcelas += 1


class PagamentoViewSet(viewsets.ModelViewSet):

    queryset = Pagamento.objects.all()
    serializer_class = PagamentoSerializer
