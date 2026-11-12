from flask import Blueprint, render_template, session, redirect, url_for, flash, Response
from auth import fazer_login, fazerCadastro, loginObrigatorio
from card import cardAtual, criarCard, acertoCard, randomCard, leitorPDF
from postit import listarNotas, criarNota, excluirNota, atualizarNota
from db import pegarUsuario

rotas_bp = Blueprint("rotas", __name__)



@rotas_bp.route("/")
def inicio():
    return render_template("index.html")

@rotas_bp.route("/robots.txt", methods=["GET"])
def robotsGoogle():
    conteudo = (
        "User-agent: *\n"
        "Allow: /\n"
        "\n"
        "Sitemap: https://senflow.duckdns.org/sitemap.xml\n"
    )
    return Response(conteudo, mimetype="text/plain")

@rotas_bp.route("/sitemap.xml", methods=["GET"])
def sitemapGoogle():
    conteudo = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://senflow.duckdns.org/</loc>
    </url>
</urlset>
"""
    return Response(conteudo, mimetype="application/xml")


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
def painel():
    usuario = pegarUsuario()
    flash(usuario)
    return render_template("home/inicial.html")
    
    
    
@rotas_bp.route("/flashcards", methods=["GET"])
@loginObrigatorio
def flashcards():
    return render_template("home/flashCards.html")

#rotas post- it
@rotas_bp.route("/postit", methods=["GET"])
@loginObrigatorio
def postit():
    return render_template("home/postit.html")

@rotas_bp.route("/api/notas", methods=["GET"])
@loginObrigatorio
def apiListarNotas():
    return listarNotas()

@rotas_bp.route("/api/notas", methods=["POST"])
@loginObrigatorio
def apiCriarNota():
    return criarNota()

@rotas_bp.route("/api/notas/<int:nota_id>", methods=["DELETE"])
@loginObrigatorio
def apiExcluirNota(nota_id):
    return excluirNota(nota_id)

@rotas_bp.route("/api/notas/<int:nota_id>", methods=["PUT"])
@loginObrigatorio
def apiAtualizarNota(nota_id):
    return atualizarNota(nota_id)

#outras rotas flashcard
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

@rotas_bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("Sessão encerada com sucesso.", "sucesso")
    return redirect(url_for("rotas.loginPage"))

@rotas_bp.route("/api/flashcards/pdf", methods=["POST"])
@loginObrigatorio
def cardpdf():
    return leitorPDF()
