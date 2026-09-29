from flask import Flask, request, render_template

# 1. Você precisa criar a instância do Flask aqui

app = Flask(__name__)

# 2. Defina a rota (URL) e o método (POST) que vai disparar a função

@app.route("/login", methods=["POST"])

def fazer_login():

    # Recebe os comandos digitados no input do Form

    user = request.form["name"]

    password = request.form["pass"]

    import sqlite3

    conexao = sqlite3.connect("meu_banco.db")

    cursor = conexao.cursor()

    cursor.execute("""

CREATE TABLE IF NOT EXISTS usuarios (

    usuario TEXT,

    senha TEXT

)gi

""")

    cursor.execute(

    "INSERT INTO usuarios (usuario, senha) VALUES (?, ?)",

    (user, password)

)

    cursor.execute(

    "SELECT usuario, senha FROM usuarios WHERE usuario = ?", #testar se o usuario esta correto

    (user,)

)

    resultados = cursor.fetchall() #Agora pegamos o resultado dentro do banco

    if resultados:

        mensagem = "Usuário encontrado!"

    else:

        mensagem = "Usuário não encontrado!"

    cursor.execute(

        "SELECT usuario, senha FROM usuarios WHERE usuario = ? AND senha = ?", #testar se a senha   ta correta

        (user, password)

    )

    resultados = cursor.fetchall()

    if resultados:

        mensagem = "Login aceito"

    else:

        mensagem = "Senha incorreta"

    conexao.commit()

    conexao.close()

    # Retorna para o HTML um texto

    return render_template(

        "login.html",

        user = "Usuario recebido: " + user,

        senha = "Senha recebida: " + password,

        mensagem = mensagem

    )

# 3. Adicione isso no final do arquivo para o servidor iniciar e continuar rodando

if __name__ == "__main__":

    app.run(debug=True)