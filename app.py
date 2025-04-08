from flask import Flask, render_template, request, redirect, send_file, jsonify
from datetime import datetime
from io import BytesIO
from escala_memoria import (
    gerar_escala,
    designar_funcionario_domingo,
    trocar_funcionarios,
    get_escala,
    exportar_csv,
)

app = Flask(__name__)

# Rota principal
@app.route("/")
def index():
    return render_template("index.html")

# Rota para gerar escala
@app.route("/gerar", methods=["POST"])
def gerar():
    try:
        data_str = request.form["data_mes"]
        data = datetime.strptime(data_str, "%Y-%m")
        gerar_escala(data.month, data.year)
        return render_template("index.html", tabela=get_escala().to_html(index=False, classes="table"))
    except Exception as e:
        return render_template("index.html", erro=f"Erro ao gerar escala: {str(e)}")

# Rota para edição (troca ou designação de domingo)
@app.route("/editar", methods=["POST"])
def editar():
    try:
        tipo = request.form["tipo_edicao"]
        data_dia = request.form["data_dia"]
        dia_formatado = datetime.strptime(data_dia, "%Y-%m-%d").strftime("%Y-%m-%d")

        if tipo == "designar":
            funcionario = request.form["funcionario_designar"]
            sucesso = designar_funcionario_domingo(dia_formatado, funcionario)
            if not sucesso:
                raise Exception("Funcionário inválido ou data incorreta.")
        elif tipo == "trocar":
            func1 = request.form["funcionario_1"]
            func2 = request.form["funcionario_2"]
            sucesso = trocar_funcionarios(dia_formatado, func1, func2)
            if not sucesso:
                raise Exception("Funcionários não encontrados para a data.")

        return render_template("index.html", tabela=get_escala().to_html(index=False, classes="table"))
    except Exception as e:
        return render_template("index.html", erro=f"Erro na edição: {str(e)}")

# Rota para exportar CSV
@app.route("/exportar", methods=["GET"])
def exportar():
    try:
        csv_data = exportar_csv()
        buffer = BytesIO(csv_data)
        buffer.seek(0)
        return send_file(
            buffer,
            mimetype="text/csv",
            as_attachment=True,
            download_name="escala.csv"
        )
    except Exception as e:
        return jsonify({"erro": f"Erro ao exportar CSV: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)
