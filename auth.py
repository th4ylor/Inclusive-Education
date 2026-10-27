from flask import request, redirect, url_for, flash, session, render_template
from db import openConnection
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash



def criar_tabela():
    conexao = openConnection()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL UNIQUE,   --UNIQUE impede email repetido
            senha_hash TEXT NOT NULL      --guarda a senha criptografada, em hash
        )
    """)

    conexao.commit()   #guarda a tabela, salva ela
    conexao.close()

def fazer_login():
    email = request.form["email"].strip().lower() #strip e lower é para caso o usuario colocar maisculo e espaço
    senha = request.form["pass"]

    conexao = openConnection()
    cursor = conexao.cursor()

    cursor.execute(
       "SELECT id, senha_hash FROM usuarios WHERE email = ?",  # select id posição 0 e senha hash posicao 1
    (email,)
)
    resultado = cursor.fetchone() #pega somente um dos resultados, aqui somente o email que eu solicitei e guarda ele na variavel
    conexao.close()
#caso o email esteja incorreto
    if resultado is None:
        flash("Email incorreto, tente novamente")
        return redirect(url_for("loginPage"))

#gurdando a senha hash numa variavel
    senha_guardada = resultado[1]  #é 2 pois na posicao 2 está a senha guardada em hash ja na posicao 0  é o id
#senha guardade = senha hash

#aqui serve para se caso o email estiver correto mas a senha não esta batendo
    if not check_password_hash(senha_guardada, senha): #checando se a senha digitada é igual a senha q virou hash
        flash("Senha incorreta, tente novamente")
        return redirect(url_for("loginPage"))
    

    session["usuario_id"] = resultado[0]   # guarda quem está logado, o 0 aqui é para o id, se for 1  é para senha hash
    flash("Login aceito")
    return redirect(url_for("Painel"))

#Isaak depois  vc tem que  conferir sobre o criar tabela, eu fiz uma função para ela e ela tem q puxar do  jeito q ta ali,
#se quiser mudar essa parte no meu codigo pode



    
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
        print("Conta adicionada ao banco de dados")
        
    #Erro que acontece quando o email ja existe
    except sqlite3.IntegrityError:
        print("Este r-mail já está cadastrado.")
        flash("Este r-mail já está cadastrado.", "erro")
        return redirect(url_for("loginPage"))
    finally:
        conn.close()
        print("Cadastro realizado! Agora faça o login.")
    flash("Cadastro realizado! Agora faça o login.", "sucesso")
    return redirect(url_for("loginPage"))
    
        
    