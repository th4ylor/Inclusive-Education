from flask import Blueprint, render_template, Flask
from auth import fazer_login, fazerCadastro, loginObrigatorio
from card import cardAtual, criarCard, acertoCard, randomCard

rotas_bp = Blueprint("rotas", __name__)



@rotas_bp.route("/")
def inicio():
    return render_template("index.html")


#Carrega a pagina de login
@rotas_bp.route("/loginPage", methods=["GET"])
def loginPage():
    print("Entrou na rota de login")
    return render_template("login.html")


@rotas_bp.route("/login", methods=["POST"])
def loginAuth():
    print("Entrou na funcao para fazer login")
    return fazer_login()

@rotas_bp.route("/cadastro", methods=["POST"])
def registerAuth():
    print("Entrou na funcao para fazer cadastro")
    return fazerCadastro()


@rotas_bp.route("/painel", methods=["GET"])
@loginObrigatorio
def Painel():
    return render_template("home/inicial.html")
    
    
    
#Rotas card
@rotas_bp.route("/flashcards", methods=["GET"])
@loginObrigatorio
def flashcards():
    return render_template("home/flashCards.html")

@rotas_bp.route("/api/flashcards/atual", methods=["GET"])
@loginObrigatorio
def apiCardAtual():
    return cardAtual()

@rotas_bp.route("/api/flashcards", methods=["POST"])
@loginObrigatorio
def apiCriarCard():
    return criarCard()

@rotas_bp.route("/api/flashcards/1", methods=["POST"])
@loginObrigatorio
def apiProxCard():
    return acertoCard()

@rotas_bp.route("/api/flashcards/2", methods=["PATCH"])
@loginObrigatorio
def apiRandom():
    return randomCard()