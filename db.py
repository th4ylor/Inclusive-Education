import sqlite3 
from flask import session

def openConnection():
    conn = sqlite3.connect("banco.db")
    
    #Permite acessar os dados do banco com "Usuarios["nome"]" ao invés de "Usuarios[0]" ou "Usuarios[1]"
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def createTable():
    conn = openConnection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL
            )
            """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS flashcards(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER  NOT NULL,
                materia TEXT NOT NULL DEFAULT 'GERAL',
                pergunta TEXT NOT NULL,
                resposta TEXT NOT NULL,
                
                FOREIGN KEY (usuario_id)
                    REFERENCES usuarios(id)
                    ON DELETE CASCADE
            )
            """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS notas(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario_id INTEGER NOT NULL,
                titulo TEXT NOT NULL,
                conteudo TEXT NOT NULL,
                cor TEXT NOT NULL DEFAULT '#f6d73ef2',
                FOREIGN KEY (usuario_id)
                    REFERENCES usuarios(id)
                    ON DELETE CASCADE
            )
        """)
        
        conn.commit()
    finally:
        conn.close()
    
def salvarFlashcards(mat, per, resp):
    usuario_id = session.get["usuario_id"]
    if not usuario_id:
        return False
    
    conn = openConnection()
    try:
        conn.execute("""
            INSERT INTO flashcards 
            (id-usuario, materia, pergunta, resposta)
            VALUES (?, ?, ?, ?)
                    """, (usuario_id, mat, per, resp))
        conn.commit()
        return True
    finally:
        conn.close()

def salvarNota(titulo, conteudo, cor):
    usuario_id = session.get("usuario_id")

    if not usuario_id:
        return False

    conn = openConnection()
    try:
        conn.execute("""
            INSERT INTO notas (usuario_id, titulo, conteudo, cor)
            VALUES (?, ?, ?, ?)
        """, (usuario_id, titulo, conteudo, cor))

        conn.commit()
        return True
    finally:
        conn.close()
        
def pegarUsuario():
    usuario_id = session.get("usuario_id")
    if not usuario_id:
        return False
    
    conn = openConnection()
    try:
        usuario = conn.execute("SELECT nome FROM usuarios WHERE id = ?", (usuario_id,)).fetchone()
        return usuario['nome']
    finally:
        conn.close()
        
        
    