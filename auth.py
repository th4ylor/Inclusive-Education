from flask import request, render_template

def fazer_login():
    if request.method == "GET":
        return render_template("login.html")
    
    #Recebe os comandos digitado no input do Form
    user = request.form["name"]
    pwd = request.form["pass"]
    
    #Retorna para o HTML um texto
    return render_template(
        "login.html",
        user = "Usuario recebido: "+ user,
        senha = "Senha recebida: "+ pwd
    )