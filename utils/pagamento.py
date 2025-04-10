from utils.escala_utils import carregar_escalas
from datetime import datetime

SALARIO_MINIMO = 1418.00
CARGA_MENSAL = 220

def calcular_relatorio_pagamento(mes, ano):
    dados = carregar_escalas()
    chave = f"{ano}-{mes:02d}"
    if chave not in dados:
        return {}

    total_por_funcionario = {}

    for dia, funcionario in dados[chave].items():
        if funcionario not in total_por_funcionario:
            total_por_funcionario[funcionario] = 0
        total_por_funcionario[funcionario] += 1  # 1 dia = 1 turno de 6h

    relatorio = {}

    for funcionario, dias_trabalhados in total_por_funcionario.items():
        horas = dias_trabalhados * 6
        proporcional = (horas / CARGA_MENSAL) * SALARIO_MINIMO
        relatorio[funcionario] = {
            "dias": dias_trabalhados,
            "horas": horas,
            "valor": round(proporcional, 2)
        }

    return relatorio
