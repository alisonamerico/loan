from django.contrib import admin
from fintech.api.models import Emprestimo, Pagamento


@admin.register(Emprestimo)
class EmprestimoAdmin(admin.ModelAdmin):
    """
    It will be defined which fields will be displayed
    in the Emprestimo view in the Admin
    """
    list_display = ('cliente', 'valor_nominal', 'taxa_juros', 'periodo',
                    'endereco_ip', 'banco', 'data_solicitacao_emprestimo')
    search_fields = ['cliente', 'endereco_ip', 'taxa_juros', 'banco', 'data_solicitacao_emprestimo']
    ordering = ('-cliente',)


@admin.register(Pagamento)
class PagamentoAdmin(admin.ModelAdmin):
    """
    It will be defined which fields will be displayed
    in the Pagamento view in the Admin
    """
    list_display = ('emprestimo_id', 'data_pagamento', 'valor_pagamento')
    search_fields = ['emprestimo_id', 'data_pagamento', 'valor_pagamento']
    ordering = ('-data_pagamento',)
