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

    def calcula_amortizacao_de_emprestimo(valor_nominal, taxa_juros, periodo):
        taxa_juros = taxa_juros / 100
        valor_parcela = (valor_nominal * taxa_juros) / (1 - (1 / (1 + taxa_juros) ** periodo))
        valor_juros_em_reais = valor_nominal * taxa_juros
        amortizacao = valor_parcela - valor_juros_em_reais
        saldo_devedor = valor_nominal - amortizacao
        return (valor_parcela, valor_juros_em_reais, saldo_devedor)

    def agendamento_de_amortizacao(valor_nominal, taxa_juros, periodo, calcula_amortizacao_de_emprestimo):
        for numero_parcelas in range(periodo, 0, -1):
            lista_valor_parcela = []
            lista_amortizacao = []
            lista_taxa_juros_em_reais = []
            lista_saldo_devedor = []
            valor_parcela, amortizacao, valor_juros_em_reais, saldo_devedor,\
                valor_nominal = calcula_amortizacao_de_emprestimo(
                    valor_nominal, taxa_juros, numero_parcelas)
            lista_valor_parcela.append(valor_parcela)
            lista_amortizacao.append(amortizacao)
            lista_taxa_juros_em_reais.append(valor_juros_em_reais)
            lista_saldo_devedor.append(saldo_devedor)
            lista_saldo_devedor.append(valor_nominal)

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
        'api.Emprestimo', related_name='emprestimo_pagamento', on_delete=models.SET_NULL,
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
