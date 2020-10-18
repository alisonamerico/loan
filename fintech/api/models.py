from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


class Emprestimo(models.Model):
    """
    Esta classe contém a representação dos campos da tabela Emprestimo.
    """

    valor_nominal = models.DecimalField(
        verbose_name='Valor inicial do empréstimo', max_digits=8, decimal_places=2
    )
    taxa_juros = models.FloatField(
        verbose_name='Taxa de Juros (%)', default=0, validators=[MinValueValidator(0)]
    )
    periodo = models.IntegerField(verbose_name='Período (Número de Meses)')
    endereco_ip = models.GenericIPAddressField(verbose_name='Endereço IP do cliente', protocol='IPV4')
    data_solicitacao_emprestimo = models.DateTimeField(
        verbose_name='Data que o empréstimo foi solicitado', auto_now_add=True)
    banco = models.CharField(verbose_name='Banco', max_length=50)
    cliente = models.OneToOneField(
        get_user_model(), verbose_name='Nome do cliente', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = 'Emprestimo'
        verbose_name_plural = 'Emprestimos'
        ordering = ['data_solicitacao_emprestimo']

    def __str__(self):
        """A string representation of the model."""
        return f'{self.cliente}, {self.valor_nominal}, {self.data_solicitacao_emprestimo}'

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

    def cronograma_de_amortizacao(valor_nominal, calcula_valor_amortizacao,
                                  calcula_saldo_devedor, periodo
                                  ):
        """
        Função que gera uma lista com os valores de:
        periodo (meses) | valor_parcela | amortizacao | valor_juros_em_reais | saldo_devedor
        :param valor_nominal: Valor total que resta pagar ou saldo devedor em cada periodo.
        :param calcula_valor_amortizacao: Função que calcula o valor da amortização.
        :param taxa_juros_percentual: Valor da taxa de juros em percentual esperada.
        :param periodo: Número de meses
        :return Retorna periodo (meses), valor_parcela, amortizacao, valor_juros_em_reais, saldo_devedor
        enquanto o número de parcelas a serem pagas forem menores que o período acordado para ser pago.
        """
        numero_parcelas = 1
        valor_amortizacao = calcula_valor_amortizacao
        saldo_devedor = calcula_saldo_devedor
        while numero_parcelas <= periodo:  # <-- parei aqui
            # valor_nominal = saldo_devedor
            # yield numero_parcelas, valor_amortizacao, valor_nominal, saldo_devedor \
            #     if saldo_devedor > 0 else 0
            # numero_parcelas += 1

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


class Pagamento(models.Model):
    """
    Esta classe contém a representação dos campos da mesa de Pagamento.
    """
    emprestimo_id = models.ForeignKey(
        'api.Emprestimo', related_name='emprestimo_pagamento', on_delete=models.DO_NOTHING,
        null=True, default=None, blank=True
    )
    data_pagamento = models.DateTimeField(verbose_name='Data do Pagamento', auto_now_add=True)
    valor_pagamento = models.DecimalField(
        verbose_name='Valor do Pagamento', max_digits=8, decimal_places=2
    )

    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'

    def __str__(self):
        """A string representation of the model."""
        return f'{self.emprestimo_id}, {self.data_pagamento}, {self.valor_pagamento}'
