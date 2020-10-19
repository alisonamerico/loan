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
