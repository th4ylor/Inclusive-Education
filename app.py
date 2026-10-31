from flask import Flask
from rotas import rotas_bp
from db import createTable
from metodologias import metodologias_bp


app = Flask(__name__)
app.register_blueprint(metodologias_bp)

app.config["SECRET_KEY"] = "chaveExpostadePropositoPorEnquanto"

createTable()

app.register_blueprint(rotas_bp)

app.run(debug=True)