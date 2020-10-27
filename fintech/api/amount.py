def calcula_amortizacao_de_emprestimo(valor_nominal, taxa_juros, periodo):
    taxa_juros = taxa_juros / 100
    valor_parcela = (valor_nominal * taxa_juros) / (1 - (1 / (1 + taxa_juros) ** periodo))
    valor_juros_em_reais = valor_nominal * taxa_juros
    amortizacao = valor_parcela - valor_juros_em_reais
    saldo_devedor = valor_nominal - amortizacao
    return (valor_parcela, valor_juros_em_reais, saldo_devedor)
