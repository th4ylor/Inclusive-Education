from flask import Flask, render_template, request
from auth import fazer_login

app = Flask(__name__)

#Inicia o site logo pela pagina de inicio: index.html
@app.route("/")
def inicio():
    return render_template("index.html")

#Carrega a pagina de login
@app.route("/loginPage", methods=["GET"])
def loginPage():
    return render_template("login.html")

@app.route("/login", methods=["POST"])
def loginAuth():
    return fazer_login()

app.run(debug=True)