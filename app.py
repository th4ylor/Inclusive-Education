from flask import Flask, render_template, request
from auth import fazer_login, fazerCadastro
from db import createTable
from card import cardAtual, criarCard, proxCard

app = Flask(__name__)

app.config["SECRET_KEY"] = "chaveExpostadePropositoPorEnquanto"

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


@app.route("/Painel", methods=["GET"])
def Painel():
    return render_template("home/inicial.html")
    
    
#Rotas card
@app.route("/flashcards", methods=["GET"])
def flashcards():
    return render_template("home/flashCards.html")

@app.route("/api/flashcards/atual", methods=["GET"])
def apiCardAtual():
    return cardAtual()

@app.route("/api/flashcards", methods=["POST"])
def apiCriarCard():
    return criarCard()

@app.route("/api/flashcards/proximo", methods=["POST"])
def apiProxCard():
    return proxCard()

app.run(debug=True)