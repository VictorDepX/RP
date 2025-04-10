from datetime import datetime
from reportlab import *
import json
import os

CAMINHO_ESCALAS = "data/escalas"

def listar_escalas():
    escalas = []
    if not os.path.exists(CAMINHO_ESCALAS):
        return escalas

    for nome_arquivo in os.listdir(CAMINHO_ESCALAS):
        if nome_arquivo.endswith(".json"):
            caminho = os.path.join(CAMINHO_ESCALAS, nome_arquivo)
            with open(caminho, 'r', encoding='utf-8') as f:
                try:
                    escala = json.load(f)
                    escalas.append(escala)
                except json.JSONDecodeError:
                    print(f"Erro ao carregar: {nome_arquivo}")
    return escalas

def salvar_escala(mes, ano, escala):
    nome_arquivo = f"escala_{ano}_{mes}.json"
    path = os.path.join(CAMINHO_ESCALAS, nome_arquivo)
    os.makedirs(CAMINHO_ESCALAS, exist_ok=True)  
    with open(path, "w", encoding="utf-8") as f:
        json.dump(escala, f, indent=4, ensure_ascii=False)

def carregar_escala(ano, mes):
    caminho = f"escalas/escala_{ano}_{mes}.json"
    if not os.path.exists(caminho):
        return None
    with open(caminho, "r", encoding="utf-8") as f:
        escala = json.load(f)
    escala.setdefault("ano", ano)
    escala.setdefault("mes", mes)
    return escala


def listar_escalas_salvas():
    os.makedirs(CAMINHO_ESCALAS, exist_ok=True)
    arquivos = [f for f in os.listdir(CAMINHO_ESCALAS) if f.endswith(".json")]
    escalas = []
    for arq in arquivos:
        partes = arq.replace("escala_", "").replace(".json", "").split("_")
        if len(partes) == 2:
            ano, mes = partes
            escalas.append((int(mes), int(ano)))
    escalas.sort(key=lambda x: (x[1], x[0]), reverse=True)
    return escalas

def exportar_pdf(escala, mes, ano):
    nome_arquivo = f"escala_{mes}_{ano}.pdf"
    caminho = os.path.join("data", nome_arquivo)

    c = canvas.Canvas(caminho, pagesize=landscape(letter))
    c.setFont("Helvetica-Bold", 14)
    c.drawString(30, 550, f"Escala de Trabalho - {mes}/{ano}")
    
    # Cabeçalho da tabela
    dados_tabela = [["Data", "Funcionário", "Horário"]]
    for dia in sorted(escala.keys(), key=lambda d: datetime.strptime(d, "%Y-%m-%d")):
        for turno in escala[dia]:
            dados_tabela.append([dia, turno["funcionario"], turno["horario"]])
    
    tabela = Table(dados_tabela, colWidths=[120, 200, 200])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ]))

    tabela.wrapOn(c, 800, 600)
    tabela.drawOn(c, 30, 100)
    c.save()

    return caminho