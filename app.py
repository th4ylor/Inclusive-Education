from flask import Flask, render_template, request
from auth import fazer_login

app = Flask(__name__)

#Inicia o site logo pela pagina de inicio: index.html
@app.route("/")
def inicio():
    return render_template("index.html")

#Carrega a pagina de login ou os comandos para login caso seja um POST do Form
@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "GET":
            return render_template("login.html")
    return fazer_login()

app.run(debug=True)