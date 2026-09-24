from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    
    if request.method == "GET":
        return render_template("login.html")
    
    usuario = request.form["name"]
    senha = request.form["pass"]
    return render_template(
        "login.html",
        user = "Usuario recebido: "+ usuario,
        senha = "Senha recebida: "+ senha
    )



app.run(debug=True)