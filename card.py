from flask import jsonify, request, session
import random
from db import openConnection

baralho = []
posicao = 0



def cardAtual():
    carregarCard()
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
    usuario_id = session.get("usuario_id")
    
    if not pergunta or not resposta:
        return jsonify({"erro": "Preencha todos os campos."}),400

    conn = openConnection()
    try:
        cursor = conn.execute("""
            INSERT INTO flashcards 
                (usuario_id, materia, pergunta, resposta)  
            VALUES (?, ?, ?, ?)
                     """, (usuario_id, materia.upper(), pergunta, resposta))
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
    card_id = baralho[posicao]["id"]
    usuario_id = session.get("usuario_id")
    conn = openConnection()
    conn.execute("DELETE FROM flashcards WHERE id = ? AND usuario_id = ?", (card_id, usuario_id))
    conn.commit()
    conn.close()
    carregarCard()
    return
    
def randomCard():
    print("TESTE MEU FII", len(baralho))
    global posicao
    anterior = posicao
    posicao = random.randrange(len(baralho))
    while posicao == anterior:
        posicao = random.randrange(len(baralho))
    return jsonify({"card" : baralho[posicao]})

def carregarCard():
    global posicao
    usuario_id = session.get("usuario_id")
    
    conn = openConnection()
    
    cursor = conn.execute(" SELECT * FROM flashcards WHERE usuario_id = ?", (usuario_id,))
    resultado = cursor.fetchall()
    baralho.clear()
    baralho.extend(dict(linha) for linha in resultado)
    posicao = 0
    conn.close()
    return