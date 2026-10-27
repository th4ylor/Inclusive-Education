from flask import Blueprint, jsonify, request, render_template, session
import math
import time

metodologias_bp = Blueprint("metodologias", __name__)

METODOLOGIAS = [
    {
        "id": "pomodoro",
        "nome": "Pomodoro",
        "descricao": "Ciclos curtos de foco intercalados com pausas breves.",
        "tipo": "tempo",
        "ciclo": [
            {"fase": "foco", "duracao_min": 25},
            {"fase": "pausa", "duracao_min": 5}
        ]
    },
    {
        "id": "foco_curto",
        "nome": "Foco Curto",
        "descricao": "Ciclos de 15 minutos para começar sem pressão, ideal para dias de pouca energia.",
        "tipo": "tempo",
        "ciclo": [
            {"fase": "foco", "duracao_min": 15},
            {"fase": "pausa", "duracao_min": 3}
        ]
    },
    {
        "id": "blocos",
        "nome": "Estudo em Blocos",
        "descricao": "Blocos mais longos de foco com pausas maiores.",
        "tipo": "tempo",
        "ciclo": [
            {"fase": "foco", "duracao_min": 50},
            {"fase": "pausa", "duracao_min": 10}
        ]
    },
    {
        "id": "feynman",
        "nome": "Técnica Feynman",
        "descricao": "Explique o conteúdo com suas próprias palavras para identificar lacunas.",
        "tipo": "passos",
        "passos": [
            "Escolha o tema que quer estudar",
            "Explique como se fosse para uma criança",
            "Identifique os pontos que você não conseguiu explicar bem",
            "Volte ao material, simplifique e repita"
        ]
    },
    {
        "id": "repeticao_espacada",
        "nome": "Repetição Espaçada",
        "descricao": "Revisões em intervalos crescentes para fixar o conteúdo.",
        "tipo": "passos",
        "passos": [
            "Revise o conteúdo",
            "Marque a dificuldade sentida (fácil, médio, difícil)",
            "Aguarde o intervalo sugerido antes da próxima revisão"
        ]
    }
]


def buscar_metodologia(metodologia_id):
    for m in METODOLOGIAS:
        if m["id"] == metodologia_id:
            return m
    return None


def tempo_decorrido(sessao):
    referencia = sessao["inicio_pausa"] if sessao["pausado"] else time.time()
    return referencia - sessao["inicio_fase"] - sessao["tempo_pausado_total"]


def segundos_focados_total(sessao, metodologia):
    total = sessao["segundos_focados"]
    fase = metodologia["ciclo"][sessao["indice_ciclo"]]
    if fase["fase"] == "foco":
        total += min(tempo_decorrido(sessao), fase["duracao_min"] * 60)
    return total


def passos_concluidos(sessao, metodologia):
    if sessao["concluida"]:
        return len(metodologia["passos"])
    return sessao["indice_passo"]


@metodologias_bp.route("/estudo", methods=["GET"])
def pagina_estudo():
    return render_template("home/estudo.html")


@metodologias_bp.route("/metodologias", methods=["GET"])
def listar_metodologias():
    return jsonify(METODOLOGIAS)


@metodologias_bp.route("/sessoes/iniciar", methods=["POST"])
def iniciar_sessao():
    dados = request.get_json(silent=True) or {}
    metodologia = buscar_metodologia(dados.get("metodologia_id"))
    if metodologia is None:
        return jsonify({"erro": "metodologia não encontrada"}), 404

    sessao = {
        "metodologia_id": metodologia["id"],
        "tipo": metodologia["tipo"],
        "objetivo": str(dados.get("objetivo", "")).strip()[:120],
        "concluida": False
    }

    if metodologia["tipo"] == "tempo":
        sessao.update({
            "indice_ciclo": 0,
            "inicio_fase": time.time(),
            "pausado": False,
            "inicio_pausa": None,
            "tempo_pausado_total": 0,
            "segundos_focados": 0,
            "ciclos_concluidos": 0
        })
    else:
        sessao["indice_passo"] = 0

    session["estudo"] = sessao
    return jsonify(sessao)


@metodologias_bp.route("/sessoes/status", methods=["GET"])
def status_sessao():
    sessao = session.get("estudo")
    if sessao is None:
        return jsonify({"erro": "nenhuma sessão ativa"}), 404

    metodologia = buscar_metodologia(sessao["metodologia_id"])
    resposta = dict(sessao)
    resposta["nome_metodologia"] = metodologia["nome"]

    if sessao["tipo"] == "tempo":
        fase = metodologia["ciclo"][sessao["indice_ciclo"]]
        duracao = fase["duracao_min"] * 60
        resposta["fase"] = fase["fase"]
        resposta["duracao_fase_segundos"] = duracao
        resposta["tempo_restante_segundos"] = max(0, math.ceil(duracao - tempo_decorrido(sessao)))
        resposta["minutos_focados"] = int(segundos_focados_total(sessao, metodologia) // 60)
    else:
        resposta["passo_atual"] = metodologia["passos"][sessao["indice_passo"]]
        resposta["total_passos"] = len(metodologia["passos"])

    return jsonify(resposta)


@metodologias_bp.route("/sessoes/pausar", methods=["POST"])
def pausar_sessao():
    sessao = session.get("estudo")
    if sessao is None or sessao["tipo"] != "tempo":
        return jsonify({"erro": "não é possível pausar"}), 400
    if not sessao["pausado"]:
        sessao["pausado"] = True
        sessao["inicio_pausa"] = time.time()
        session["estudo"] = sessao
    return jsonify(sessao)


@metodologias_bp.route("/sessoes/retomar", methods=["POST"])
def retomar_sessao():
    sessao = session.get("estudo")
    if sessao is None or sessao["tipo"] != "tempo":
        return jsonify({"erro": "não é possível retomar"}), 400
    if sessao["pausado"]:
        sessao["tempo_pausado_total"] += time.time() - sessao["inicio_pausa"]
        sessao["pausado"] = False
        sessao["inicio_pausa"] = None
        session["estudo"] = sessao
    return jsonify(sessao)


@metodologias_bp.route("/sessoes/avancar", methods=["POST"])
def avancar_sessao():
    sessao = session.get("estudo")
    if sessao is None:
        return jsonify({"erro": "nenhuma sessão ativa"}), 404

    metodologia = buscar_metodologia(sessao["metodologia_id"])

    if sessao["tipo"] == "tempo":
        fase = metodologia["ciclo"][sessao["indice_ciclo"]]
        duracao = fase["duracao_min"] * 60
        decorrido = min(tempo_decorrido(sessao), duracao)
        if fase["fase"] == "foco":
            sessao["segundos_focados"] += decorrido
            if decorrido >= duracao:
                sessao["ciclos_concluidos"] += 1
        sessao["indice_ciclo"] = (sessao["indice_ciclo"] + 1) % len(metodologia["ciclo"])
        sessao["inicio_fase"] = time.time()
        sessao["pausado"] = False
        sessao["inicio_pausa"] = None
        sessao["tempo_pausado_total"] = 0
    elif sessao["indice_passo"] + 1 < len(metodologia["passos"]):
        sessao["indice_passo"] += 1
    else:
        sessao["concluida"] = True

    session["estudo"] = sessao
    return jsonify(sessao)


@metodologias_bp.route("/sessoes/encerrar", methods=["POST"])
def encerrar_sessao():
    sessao = session.pop("estudo", None)
    resposta = {"mensagem": "sessão encerrada"}

    if sessao is not None:
        metodologia = buscar_metodologia(sessao["metodologia_id"])
        if sessao["tipo"] == "tempo":
            resposta["minutos_focados"] = int(segundos_focados_total(sessao, metodologia) // 60)
            resposta["ciclos_concluidos"] = sessao["ciclos_concluidos"]
        else:
            resposta["passos_concluidos"] = passos_concluidos(sessao, metodologia)

    return jsonify(resposta)
