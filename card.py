from flask import jsonify, request, session
import random
from db import openConnection

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
    id_usuario = session.get("id_usuario")
    
    if not pergunta or not resposta:
        return jsonify({"erro": "Preencha todos os campos."}),400

    conn = openConnection()
    try:
        cursor = conn.execute("""
            INSERT INTO flashcards 
                (id_usuario, materia, pergunta, resposta)  
            VALUES (?, ?, ?, ?)
                     """, (id_usuario, materia.upper(), pergunta, resposta))
        conn.commit()
        card_id = cursor.lastrowid    
        return jsonify({
            "card": {
            "id" : card_id,
            "materia" : materia,
            "pergunta": pergunta,
            "resposta" : resposta
            }
        })
    finally:
        conn.close()

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
    