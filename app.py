from flask import Flask, render_template, request
from auth import fazer_login, fazerCadastro
from db import createTable

app = Flask(__name__)

app.config["SECRET_KEY"] = "capscoy17"

createTable()

#Inicia o site logo pela pagina de inicio: index.html
@app.route("/")
def inicio():
    return render_template("index.html")


#Carrega a pagina de login
@app.route("/loginPage", methods=["GET"])
def loginPage():
    print("Entrou na rota de login")
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def loginAuth():
    print("Entrou na funcao para fazer login")
    return fazer_login()

@app.route("/cadastro", methods=["POST"])
def registerAuth():
    print("Entrou na funcao para fazer cadastro")
    return fazerCadastro()


app.run(debug=True)