from rest_framework import serializers
from fintech.api.models import Emprestimo, Pagamento
from django.core.validators import MinValueValidator


class PagamentoSerializer(serializers.ModelSerializer):

    """
    EmprestimoSerializer - It will be defined which fields
    will be displayed in the Pagamento view.
    """

    emprestimo = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    data_pagamento = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")

    class Meta:
        model = Pagamento
        fields = ('id', 'emprestimo', 'data_pagamento', 'valor_pagamento')


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
    data_solicitacao_emprestimo = serializers.DateTimeField(format="%d-%m-%Y %H:%M:%S")
    banco = serializers.CharField(max_length=50)
    pagamentos = PagamentoSerializer(many=True, required=False)

    class Meta:
        model = Emprestimo
        fields = ('id', 'cliente', 'valor_nominal', 'taxa_juros',
                  'periodo', 'endereco_ip', 'data_solicitacao_emprestimo', 'banco', 'pagamentos')
