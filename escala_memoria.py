from datetime import datetime, timedelta
import calendar
import pandas as pd

# Funcionários disponíveis
FUNCIONARIOS = ["Ruth", "João Gabriel", "Victor"]

# Turnos fixos
TURNOS_SEMANA = [("05:00", "11:00"), ("11:00", "17:00"), ("16:00", "22:00")]
TURNOS_SABADO = [("06:00", "10:00"), ("10:00", "14:00"), ("13:00", "17:00")]
TURNO_EXTRA_DOMINGO = ("09:00", "12:00")

# Escala em memória
escala_df = pd.DataFrame(columns=["Data", "Funcionário", "Início", "Fim"])

# Geração da escala
def gerar_escala(mes: int, ano: int):
    global escala_df
    primeiro_dia = datetime(ano, mes, 1)
    ultimo_dia = datetime(ano, mes, calendar.monthrange(ano, mes)[1])
    delta = timedelta(days=1)
    ordem_funcionarios = FUNCIONARIOS.copy()
    escala = []

    data_atual = primeiro_dia
    while data_atual <= ultimo_dia:
        dia_semana = data_atual.weekday()
        data_str = data_atual.strftime('%Y-%m-%d')

        if dia_semana < 5:  # Segunda a sexta
            for i, func in enumerate(FUNCIONARIOS):
                escala.append([data_str, func, *TURNOS_SEMANA[i]])
        elif dia_semana == 5:  # Sábado
            for i, turno in enumerate(TURNOS_SABADO):
                func = ordem_funcionarios[i]
                escala.append([data_str, func, *turno])
            ordem_funcionarios.append(ordem_funcionarios.pop(0))
        elif dia_semana == 6:  # Domingo
            escala.append([data_str, "-", *TURNO_EXTRA_DOMINGO])

        data_atual += delta

    escala_df = pd.DataFrame(escala, columns=["Data", "Funcionário", "Início", "Fim"])
    return escala_df

# Designar funcionário no domingo
def designar_funcionario_domingo(dia, funcionario):
    global escala_df
    if funcionario in FUNCIONARIOS:
        escala_df.loc[(escala_df["Data"] == dia) & (escala_df["Funcionário"] == "-"), "Funcionário"] = funcionario
        return True
    return False

# Trocar funcionários em um mesmo dia
def trocar_funcionarios(dia, func1, func2):
    global escala_df
    mask1 = (escala_df["Data"] == dia) & (escala_df["Funcionário"] == func1)
    mask2 = (escala_df["Data"] == dia) & (escala_df["Funcionário"] == func2)

    if mask1.any() and mask2.any():
        escala_df.loc[mask1, "Funcionário"] = func2
        escala_df.loc[mask2, "Funcionário"] = func1
        return True
    return False

# Retornar a escala atual
def get_escala():
    global escala_df
    return escala_df

# Exportar para CSV
def exportar_csv():
    global escala_df
    return escala_df.to_csv(index=False).encode("utf-8")
