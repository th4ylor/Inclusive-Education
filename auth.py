from flask import request, redirect, url_for, flash, session
from db import openConnection
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def fazer_login():
    
    #Recebe os comandos digitado no input do Form
    email = request.form["email"]
    pwd = request.form["pass"]
    
    #Retorna para o HTML um texto
    return render_template(
        "login.html",
        user = "Usuario recebido: "+ email,
        senha = "Senha recebida: "+ pwd
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
        
    