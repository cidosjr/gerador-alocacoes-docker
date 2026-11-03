from flask import Flask, render_template, request, Response
from io import StringIO
import csv
import re

app = Flask(__name__)

DIAS = ["23", "24", "25"]
LOCAIS = ["03", "04"]
HORARIOS = ["08", "10", "13", "16", "19"]
SESSOES = ["A", "B", "C", "D", "E"]

def interpretar_salas(texto):
    itens = re.split(r"[\s,;]+", texto.strip())
    salas = []
    invalidas = []
    for item in filter(None, itens):
        if re.fullmatch(r"\d{1,3}", item):
            sala = item.zfill(3)
            if sala not in salas:
                salas.append(sala)
        else:
            invalidas.append(item)
    return salas, invalidas

def gerar_codigos(salas, local_escolhido):
    codigos = []
    for dia in DIAS:
        for local in [local_escolhido]:
            for sala in salas:
                for horario in HORARIOS:
                    for sessao in SESSOES:
                        codigos.append({
                            "dia": dia,
                            "local": local,
                            "sala": sala,
                            "horario": horario,
                            "sessao": sessao,
                            "codigo": f"{dia}, {local}, {sala}, {horario}{sessao}"
                        })
    return codigos

@app.route("/", methods=["GET", "POST"])
def index():
    texto_salas = ""
    salas = []
    invalidas = []
    codigos = []
    local_escolhido = "03"
    if request.method == "POST":
        texto_salas = request.form.get("salas", "")
        local_escolhido = request.form.get("local", "03")
        if local_escolhido not in LOCAIS:
            local_escolhido = "03"
        salas, invalidas = interpretar_salas(texto_salas)
        codigos = gerar_codigos(salas, local_escolhido)
    return render_template(
        "index.html",
        texto_salas=texto_salas,
        salas=salas,
        invalidas=invalidas,
        codigos=codigos,
        total=len(codigos),
        locais=LOCAIS,
        local_escolhido=local_escolhido
    )

@app.post("/download")
def download():
    texto_salas = request.form.get("salas", "")
    salas, _ = interpretar_salas(texto_salas)
    local_escolhido = request.form.get("local", "03")
    if local_escolhido not in LOCAIS:
        local_escolhido = "03"
    codigos = gerar_codigos(salas, local_escolhido)

    output = StringIO()
    writer = csv.writer(output, delimiter=";")
    writer.writerow(["Dia", "Local", "Sala", "Horario", "Sessao", "Codigo"])
    for item in codigos:
        writer.writerow([
            item["dia"], item["local"], item["sala"],
            item["horario"], item["sessao"], item["codigo"]
        ])

    return Response(
        "\ufeff" + output.getvalue(),
        mimetype="text/csv; charset=utf-8",
        headers={"Content-Disposition": "attachment; filename=codigos_alocacao.csv"}
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
