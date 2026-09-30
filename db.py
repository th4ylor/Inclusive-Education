import sqlite3 

def openConnection():
    conn = sqlite3.connect("banco.db")
    
    #Permite acessar os dados do banco com "Usuarios["nome"]" ao invés de "Usuarios[0]" ou "Usuarios[1]"
    conn.row_factory = sqlite3.Row
    return conn

def createTable():
    conn = openConnection()
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS usuarios(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL UNIQUE,
                senha_hash TEXT NOT NULL,
                criado_em TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """)
        conn.commit()
    finally:
        conn.close()