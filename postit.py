from flask import jsonify, session, request
from db import openConnection

def listarNotas():
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return jsonify({"erro": "Usuário não autenticado."}), 401

    conn = openConnection()
    try:
        resultado = conn.execute("""
            SELECT id, titulo, conteudo, cor
            FROM notas
            WHERE usuario_id = ?
            ORDER BY id DESC
        """, (usuario_id,)).fetchall()

        notas = [dict(nota) for nota in resultado]

        return jsonify({"notas": notas})
    finally:
        conn.close()

def criarNota():
    dados = request.get_json()

    titulo = dados.get("titulo")
    conteudo = dados.get("conteudo")
    cor = dados.get("cor", "#f6d73ef2")

    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return jsonify({"erro": "Usuário não autenticado."}), 401

    if not titulo or not conteudo or not titulo.strip() or not conteudo.strip():
        return jsonify({"erro": "Preencha o título e o conteúdo."}), 400

    titulo = titulo.strip()
    conteudo = conteudo.strip()

    conn = openConnection()

    try:
        cursor = conn.execute("""
            INSERT INTO notas (usuario_id, titulo, conteudo, cor)
            VALUES (?, ?, ?, ?)
        """, (usuario_id, titulo, conteudo, cor))

        conn.commit()

        nota_id = cursor.lastrowid

        return jsonify({
            "mensagem": "Anotação criada com sucesso!",
            "nota": {
                "id": nota_id,
                "titulo": titulo,
                "conteudo": conteudo,
                "cor": cor
            }
        }), 201

    finally:
        conn.close()

def excluirNota(nota_id):
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return jsonify({"erro": "Usuário não autenticado."}), 401

    conn = openConnection()

    try:
        cursor = conn.execute("""
            DELETE FROM notas
            WHERE id = ? AND usuario_id = ?
        """, (nota_id, usuario_id))

        if cursor.rowcount == 0:
            return jsonify({"erro": "Anotação não encontrada."}), 404

        conn.commit()

        return jsonify({"mensagem": "Anotação excluída com sucesso!"})

    finally:
        conn.close()

def atualizarNota(nota_id):
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return jsonify({"erro": "Usuário não autenticado."}), 401

    dados = request.get_json()

    titulo = dados.get("titulo")
    conteudo = dados.get("conteudo")
    cor = dados.get("cor")

    if not titulo or not conteudo or not cor or not titulo.strip() or not conteudo.strip():
        return jsonify({"erro": "Preencha todos os campos."}), 400

    titulo = titulo.strip() 
    conteudo = conteudo.strip()

    conn = openConnection()

    try:
        cursor = conn.execute("""
            UPDATE notas
            SET titulo = ?, conteudo = ?, cor = ?
            WHERE id = ? AND usuario_id = ?
        """, (titulo, conteudo, cor, nota_id, usuario_id))

        if cursor.rowcount == 0:
            return jsonify({"erro": "Anotação não encontrada."}), 404

        conn.commit()

        return jsonify({"mensagem": "Anotação atualizada com sucesso!"})

    finally:
        conn.close()

#request permite que o Flask acesse os dados recebidos nessa requisição
#cursor.lastrowid: recupera o ID que o SQLite acabou de gerar para a anotação.
# cursor.rowcount: Informa quantas linhas foram afetadas pela consulta



