from flask import Flask, render_template, make_response
from datetime import datetime
import json

import random

def get_reviews():
    with open("static/data/reviews.json", encoding="utf-8") as f:
        reviews = json.load(f)

    # TOTAL ORIGINAL (arquivo inteiro)
    total_geral = len(reviews)

    # FILTRO
    filtradas = [
        r for r in reviews
        if r.get("nota") in [4, 5] and r.get("texto") and r.get("texto").strip() != ""
    ]

    if not filtradas:
        return [], 0, total_geral

    # SORTEAR 10 ALEATÓRIAS
    selecionadas = random.sample(filtradas, min(10, len(filtradas)))

    # MÉDIA DAS FILTRADAS
    media = round(sum(r["nota"] for r in filtradas) / len(filtradas), 1)

    return selecionadas, media, total_geral


def status_clinica():

    horarios = {
        0: ("08:00","19:00"),  # segunda
        1: ("08:00","19:00"),
        2: ("08:00","19:00"),
        3: ("08:00","19:00"),
        4: ("08:00","19:00"),
        5: ("08:00","16:00"),
        6: None               # domingo (fechado)
    }

    nomes_dias = {
        0: "segunda",
        1: "terça",
        2: "quarta",
        3: "quinta",
        4: "sexta",
        5: "sábado",
        6: "domingo"
    }

    agora = datetime.now()
    dia = agora.weekday()
    hora_atual = agora.time()

    horario = horarios[dia]

    # FUNÇÃO PRA ACHAR O PRÓXIMO DIA ABERTO
    def proximo_dia_aberto(dia_atual):
        for i in range(1, 8):
            prox = (dia_atual + i) % 7
            if horarios[prox] is not None:
                return prox, horarios[prox]
        return None, None

    # SE HOJE ESTÁ FECHADO (domingo)
    if horario is None:
        prox_dia, prox_horario = proximo_dia_aberto(dia)
        return f"Fechado — abre {nomes_dias[prox_dia]} às {prox_horario[0]}"

    abertura = datetime.strptime(horario[0], "%H:%M").time()
    fechamento = datetime.strptime(horario[1], "%H:%M").time()

    # SE ESTÁ ABERTO AGORA
    if abertura <= hora_atual <= fechamento:
        return f"Aberto agora — fecha às {horario[1]}"

    # SE JÁ PASSOU DO HORÁRIO DE HOJE → IR PRO PRÓXIMO DIA
    if hora_atual > fechamento:
        prox_dia, prox_horario = proximo_dia_aberto(dia)
        return f"Fechado — abre {nomes_dias[prox_dia]} às {prox_horario[0]}"

    # SE AINDA VAI ABRIR HOJE
    return f"Fechado — abre hoje às {horario[0]}"

app = Flask(__name__)
@app.route("/")
def home():
    reviews, media, total = get_reviews()

    html = render_template(
        "index.html", 
        status_funcionamento=status_clinica(),
        reviews=reviews,
        media=media,
        total=total
    )

    response = make_response(html)

    # HEADERS SEO IMPORTANTES
    response.headers["Cache-Control"] = "public, max-age=3600"
    response.headers["X-Robots-Tag"] = "index, follow"

    return response

if __name__ == "__main__":
    app.run(debug=True)    