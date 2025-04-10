from flask import Flask, render_template, request, redirect, url_for, send_file
from utils.gerador import *
from utils.escala_utils import *
from datetime import date

app = Flask(__name__)

@app.route("/")
def index():
    escala = carregar_escala(2025, 4)
    if not escala:
        escala = {"ano": 2024, "mes": 4, "dados": []}  # valores padrão para evitar erro
    return render_template("index.html", escala=escala, ano=escala["ano"], mes=escala["mes"])

@app.route("/gerar", methods=["GET", "POST"])
def gerar():
    if request.method == "POST":
        mes = int(request.form["mes"])
        ano = int(request.form["ano"])
        escala = gerar_escala(mes, ano)
        salvar_escala(mes, ano, escala)
        return redirect(url_for("index"))
    return render_template("gerar.html")

@app.route("/editar/<int:mes>/<int:ano>", methods=["GET", "POST"])
def editar(mes, ano):
    escala = carregar_escala(mes, ano)
    if request.method == "POST":
        data = request.form["data"]
        funcionario = request.form["funcionario"]
        escala[data] = funcionario
        salvar_escala(mes, ano, escala)
        return redirect(url_for("index"))
    return render_template("editar.html", escala=escala, mes=mes, ano=ano)

@app.route("/exportar/<int:mes>/<int:ano>")
def exportar(mes, ano):
    escala = carregar_escala(mes, ano)
    pdf_path = exportar_pdf(escala, mes, ano)
    return send_file(pdf_path, as_attachment=True)

@app.route("/pagamento/<int:mes>/<int:ano>")
def pagamento(mes, ano):
    escala = carregar_escala(mes, ano)
    pagamentos = calcular_pagamento(escala)
    return render_template("pagamento.html", pagamentos=pagamentos, mes=mes, ano=ano)

if __name__ == "__main__":
    app.run(debug=True)
