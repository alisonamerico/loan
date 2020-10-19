from rest_framework import serializers
from fintech.api.models import Emprestimo, Pagamento
from django.core.validators import MinValueValidator


class EmprestimoSerializer(serializers.Serializer):

    """
    EmprestimoSerializer - It will be defined which fields
    will be displayed in the Emprestimo view.
    """

    cliente = serializers.ReadOnlyField(source='cliente.first_name')
    valor_nominal = serializers.DecimalField(max_digits=8, decimal_places=2)
    taxa_juros = serializers.FloatField(default=0, validators=[MinValueValidator(0)])
    periodo = serializers.IntegerField()
    endereco_ip = serializers.ReadOnlyField()
    data_solicitacao_emprestimo = serializers.DateTimeField()
    banco = serializers.CharField(max_length=50)

    # emprestimos = [Emprestimo(valor_nominal=valor_nominal, taxa_juros=taxa_juros,
    #                           periodo=periodo, endereco_ip=endereco_ip,
    #                           data_solicitacao_emprestimo=data_solicitacao_emprestimo, banco=banco)]


serializer = EmprestimoSerializer(many=True)
serializer.data

# class Meta:
#     model = Emprestimo
#     fields = (
#         'id', 'cliente', 'valor_nominal', 'taxa_juros', 'periodo',
#         'endereco_ip', 'taxa_juros', 'banco'
#     )


class PagamentoSerializer(serializers.ModelSerializer):

    """
    EmprestimoSerializer - It will be defined which fields
    will be displayed in the Pagamento view.
    """

    emprestimo = serializers.ReadOnlyField()

    class Meta:
        model = Pagamento
        fields = ('id', 'emprestimo', 'data_pagamento', 'valor_pagamento')
