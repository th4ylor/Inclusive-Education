from flask import jsonify, request, session
import random
from db import openConnection

card_id = 0


def cardAtual():
    usuario_id = session.get("usuario_id")
    card_id = session.get("card_atual_id")
    
    conn = openConnection()
    resultado = conn.execute(
        "SELECT * FROM flashcards WHERE id = ? AND usuario_id = ?", (card_id, usuario_id)).fetchone()
    conn.close()
    if resultado is None :
        return randomCard()
    return jsonify({"card": dict(resultado)})
    

def criarCard():
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
    removerCard()
    return randomCard()


def removerCard():
    card_id = session.get("card_atual_id")
    usuario_id = session.get("usuario_id")
    
    if usuario_id is None or card_id is None:
        return
    
    conn = openConnection()
    conn.execute("DELETE FROM flashcards WHERE id = ? AND usuario_id = ?",
                (card_id, usuario_id))
    conn.commit()
    conn.close()
    session.pop("card_atual_id", None)
    return
    
    
def randomCard():
    usuario_id =  session.get("usuario_id")
    conn = openConnection()
    resultado = conn.execute("SELECT * FROM flashcards WHERE usuario_id = ?", (usuario_id,)).fetchall()
    conn.close()
    cards = [dict(linha) for linha in resultado]
    print(cards)
    if not cards:
        session.pop("card_atual_id", None)
        return jsonify({"card": None})
    anteriorId = session.get("card_atual_id")
    seila = [
        card for card in cards
        if card["id"] != anteriorId
    ]
    escolhido = random.choice(seila or cards)
    session["card_atual_id"] = escolhido["id"]
    return jsonify({"card": escolhido})
