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
                id_usuario INTEGER  NOT NULL,
                materia TEXT NOT NULL DEFAULT 'GERAL',
                pergunta TEXT NOT NULL,
                resposta TEXT NOT NULL,
                
                FOREIGN KEY (id_usuario)
                    REFERENCES usuarios(id)
                    ON DELETE CASCADE
            )
            """)
        
        conn.commit()
    finally:
        conn.close()
    
def salvarFlashcards(mat, per, resp):
    id_usuario = session.get["id_usuario"]
    if not id_usuario:
        return False
    
    conn = openConnection()
    try:
        conn.execute("""
            INSERT INTO flashcards 
            (id-usuario, materia, pergunta, resposta)
            VALUES (?, ?, ?, ?)
                    """, (id_usuario, mat, per, resp))
        conn.commit()
        return True
    finally:
        conn.close()