from flask import Flask, render_template, request, redirect, send_file
import pandas as pd
from datetime import datetime, timedelta
import calendar
from io import StringIO

app = Flask(__name__)

funcionarios = ["Ruth", "João Gabriel", "Victor"]
turnos_semana = [("05:00", "11:00"), ("11:00", "17:00"), ("16:00", "22:00")]
turnos_sabado = [("06:00", "10:00"), ("10:00", "14:00"), ("13:00", "17:00")]
turno_extra_domingo = ("09:00", "12:00")

df_escala = pd.DataFrame(columns=["Data", "Funcionário", "Início", "Fim"])

def gerar_escala(mes, ano):
    global df_escala
    primeiro_dia = datetime(ano, mes, 2)
    ultimo_dia = datetime(ano, mes, calendar.monthrange(ano, mes)[1])
    delta = timedelta(days=1)
    escala = []
    ordem_funcionarios = funcionarios.copy()

    data_atual = primeiro_dia
    while data_atual <= ultimo_dia:
        dia_semana = data_atual.weekday()
        data_str = data_atual.strftime('%m-%d')

        if dia_semana < 5:
            for i, func in enumerate(funcionarios):
                escala.append([data_str, func, *turnos_semana[i]])
        elif dia_semana == 5:
            for i, turno in enumerate(turnos_sabado):
                func = ordem_funcionarios[i]
                escala.append([data_str, func, *turno])
            ordem_funcionarios.append(ordem_funcionarios.pop(0))
        elif dia_semana == 6:
            escala.append([data_str, "-", *turno_extra_domingo])
        data_atual += delta

    df_escala = pd.DataFrame(escala, columns=["Data", "Funcionário", "Início", "Fim"])

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/gerar", methods=["GET", "POST"])
def gerar():
    if request.method == "POST":
        data = request.form.get("data")
        data = datetime.strptime(data, "%Y-%m")
        gerar_escala(data.month, data.year)
        tabela_html = df_escala.to_html(classes="tabela-escala", index=False)
        return render_template("resultado.html", tabela=tabela_html, mensagem="Escala gerada com sucesso.")
    return render_template("gerar.html")

@app.route("/editar", methods=["GET", "POST"])
def editar():
    mensagem = ""
    if request.method == "POST":
        acao = request.form.get("acao")
        data = request.form.get("data")
        func1 = request.form.get("func1")
        func2 = request.form.get("func2")
        if acao == "trocar" and func1 in funcionarios and func2 in funcionarios:
            mask1 = (df_escala["Data"] == data) & (df_escala["Funcionário"] == func1)
            mask2 = (df_escala["Data"] == data) & (df_escala["Funcionário"] == func2)
            if not df_escala[mask1].empty and not df_escala[mask2].empty:
                df_escala.loc[mask1, "Funcionário"], df_escala.loc[mask2, "Funcionário"] = func2, func1
                mensagem = "Troca realizada com sucesso."
        elif acao == "designar":
            func = request.form.get("func")
            if func in funcionarios:
                mask = (df_escala["Data"] == data) & (df_escala["Funcionário"] == "-")
                df_escala.loc[mask, "Funcionário"] = func
                mensagem = "Funcionário designado com sucesso."
    tabela_html = df_escala.to_html(classes="tabela-escala", index=False)
    return render_template("editar.html", tabela=tabela_html, mensagem=mensagem)

@app.route("/exportar")
def exportar():
    csv = df_escala.to_csv(index=False)
    buffer = StringIO(csv)
    buffer.seek(0)
    return send_file(buffer, mimetype="text/csv", as_attachment=True, download_name="escala.csv")

if __name__ == "__main__":
    app.run(debug=True)