from rest_framework import serializers
from fintech.api.models import Emprestimo, Pagamento


class EmprestimoSerializer(serializers.ModelSerializer):

    """
    EmprestimoSerializer - It will be defined which fields
    will be displayed in the Emprestimo view.
    """

    cliente = serializers.ReadOnlyField(source='cliente.first_name')

    class Meta:
        model = Emprestimo
        fields = (
            'id', 'cliente', 'valor_nominal', 'taxa_juros', 'periodo',
            'endereco_ip', 'taxa_juros', 'banco'
        )


class PagamentoSerializer(serializers.ModelSerializer):

    """
    EmprestimoSerializer - It will be defined which fields
    will be displayed in the Pagamento view.
    """

    emprestimo = serializers.ReadOnlyField()

    class Meta:
        model = Pagamento
        fields = ('id', 'emprestimo', 'data_pagamento', 'valor_pagamento')
