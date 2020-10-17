from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator


class Emprestimo(models.Model):
    """
    This class contains the representation of the fields in the Emprestimo table.
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

    def calcula_saldo_devedor(valor_nominal, calcula_valor_amortizacao):
        saldo_devedor = valor_nominal - calcula_valor_amortizacao
        return saldo_devedor

    def calcula_taxa_juros(valor_nominal, calcula_valor_amortizacao):
        taxa_juros = (valor_nominal * calcula_valor_amortizacao) / 100
        return taxa_juros

    def calcula_valor_parcela(valor_nominal, taxa_juros, periodo):
        valor_parcela = (valor_nominal * taxa_juros) / (1 - (1 / (1 + taxa_juros) ** periodo))
        return valor_parcela

    def calcula_valor_amortizacao(calcula_valor_parcela, calcula_taxa_juros):
        amortizacao = calcula_valor_parcela - calcula_taxa_juros
        return amortizacao

    # def calcula_valor_amortizacao_por_periodo(calcula_valor_amortizacao):
    #     valor_amortizacao = calcula_valor_amortizacao

        # def calcula_valor_amortizacao(valor_nominal, taxa_juros, periodo):
        #     """
        #     Calcula valor da Amortização por periodo
        #     :param valor_nominal: Valor inicial do empréstimo
        #     :param taxa_juros: Taxa de Juros por periodo
        #     :param periodo: Total number of periods
        #     :return: Amortização amount por periodo
        #     """
        #     x = (1 + taxa_juros) ** periodo
        #     return valor_nominal * (taxa_juros * x) / (x - 1)

        # def amortization_schedule(principal, interest_rate, period, calculate_amortization_amount):
        #     """
        #     Generates amortization schedule
        #     :param principal: Principal amount
        #     :param interest_rate: Interest rate per period
        #     :param period: Total number of periods
        #     :return: Rows containing period, interest, principal, balance, etc
        #     """
        #     amortization_amount = calculate_amortization_amount
        #     number = 1
        #     balance = principal
        #     while number <= period:
        #         interest = balance * interest_rate
        #         principal = amortization_amount - interest
        #         balance = balance - principal
        #         yield number, amortization_amount, interest, principal, balance if balance > 0 else 0
        #         number += 1

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
    This class contains the representation of the fields in the Pagamento table.
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
