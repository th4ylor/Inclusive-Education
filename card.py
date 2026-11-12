from flask import jsonify, request, session
import random
from db import openConnection
from dotenv import load_dotenv
load_dotenv()
import os
import openai
import json
import pymupdf

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
    
def criarCard(dados = None):
    if dados is None:
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
            }})
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

# cpa essa bomba vai ser integrada
# https://console.groq.com/docs/quickstart
# Todo o oodigo tirado da documentação
def textoIA(texto):
    client = openai.OpenAI(
        api_key=os.environ.get("GROQ_API_KEY"),
        base_url="https://api.groq.com/openai/v1"
    )
    resposta = client.responses.create(
        model="openai/gpt-oss-20b",
        instructions=("Extraia conteúdos do texto. O intuito é criar um flashcard com pergunta e resposta sobre o tema afins de estudo"),
        input= texto,
        text={
            "format": {
                "type": "json_schema",
                "name": "flashcards",
                "strict": True,
                "schema": {
                    "type": "object",
                    "properties": {
                        "materia": {"type": "string"},
                        "pergunta": {"type": "string"},
                        "resposta": {"type": "string"}
                    },
                    "required": ["materia", "pergunta", "resposta"],
                    "additionalProperties": False
                }}})
    flashcards = json.loads(resposta.output_text)
    return flashcards

def leitorPDF():
    print("LeitorPDF chamado")
    request.max_content_length = 10 * 1024 * 1024
    pdf = request.files.get("arquivo")
    
    if pdf is None or not pdf.filename:
        print("Caiu no if")
        return jsonify({"erro" : "Selecione um arquivo"})
    
    textos = []
    
    with pymupdf.open(stream=pdf.read(), filetype="pdf") as documento:
        for numero,pagina in enumerate(documento,start=1):
            texto = pagina.get_text()
            #print(f"Pagina {numero}: {texto}", flush=True)
            textos.append(texto)
    textoCompleto = "\n".join(textos)
    card = textoIA(textoCompleto)
    
    criar = {
        "materia": card["materia"],
        "pergunta": card["pergunta"],
        "resposta": card["resposta"]
    }
    criarCard(criar)
    
    return jsonify({"card":card})


