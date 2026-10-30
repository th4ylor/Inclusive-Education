from flask import jsonify, request
import random

baralho = []
posicao = 0


def cardAtual():
    if not baralho:
        return jsonify({"card":None})
    print(baralho)
    return jsonify({"card": baralho[posicao]})

def criarCard():
    global posicao
    dados = request.get_json(silent=True) or {}
    
    materia = (dados.get("materia") or "").strip().upper() or "GERAL"
    pergunta = (dados.get("pergunta") or "").strip()   
    resposta = (dados.get("resposta") or "").strip()
    
    if not pergunta or not resposta:
        return jsonify({"erro": "Preencha todos os campos."}),400

    card = {"materia": materia, "pergunta": pergunta, "resposta": resposta}
    baralho.append(card)
    posicao = len(baralho) - 1
    return jsonify({"card": card}),201

def acertoCard():
    global posicao
    removerCard()
    if not baralho:
        return jsonify({"card": None})
    posicao = (posicao + 1) % len(baralho)
    return jsonify({"card": baralho[posicao]})

def removerCard():
    global posicao
    del baralho[posicao]
    return
    
def randomCard():
    global posicao
    anterior = posicao
    posicao = random.randrange(len(baralho))
    while posicao == anterior:
        posicao = random.randrange(len(baralho))
    return cardAtual()
    