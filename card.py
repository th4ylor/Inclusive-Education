from flask import jsonify, request

baralho = []
posicao = 0


def cardAtual():
    if not baralho:
        return jsonify({"card":None})
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


def proxCard():
    global posicao
    
    if not baralho:
        return jsonify({"card": None})
    
    posicao = (posicao + 1) % len(baralho)
    return jsonify({"card": baralho[posicao]})