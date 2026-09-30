from flask import request, redirect, url_for, flash, session, render_template
from db import openConnection
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

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
    
def fazerCadastro():
    name = request.form["nome"].strip()
    email = request.form["email"].strip()
    senha = request.form["senha"].strip()
    confSenha = request.form["confSenha"].strip()
    
    #Validando os dados
    if not name or not email or not senha :
        flash("Preencha todos os campos.", "erro")
        return redirect(url_for("loginPage"))
    if "@" not in email or "." not in email:
        flash("Digite um e-mail válido", "erro")
        return redirect(url_for("loginPage"))
    if len(senha) < 8:
        flash("A senha deve conter no mínimo 8 caracteres.", "erro")
        return redirect(url_for("loginPage"))
    if senha != confSenha:
        flash("As senhas não coincidem", "erro")
        return redirect(url_for("loginPage"))
    
    hashSenha = generate_password_hash(senha)
    
    conn = openConnection()
    try:
        conn.execute(
            "INSERT INTO usuarios (nome, email, senha_hash) VALUES (?, ?, ?)",
            (name, email, hashSenha))
        conn.commit()
        
    #Erro que acontece quando o email ja existe
    except sqlite3.IntegrityError:
        flash("Este r-mail já está cadastrado.", "erro")
        return redirect(url_for("loginPage"))
    finally:
        conn.close()
        
    flash("Cadastro realizado! Agora faça o login.", "sucesso")
    return redirect(url_for("loginPage"))
        
    