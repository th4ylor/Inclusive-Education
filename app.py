from flask import Flask
from rotas import rotas_bp
from db import createTable

app = Flask(__name__)

app.config["SECRET_KEY"] = "chaveExpostadePropositoPorEnquanto"

createTable()

app.register_blueprint(rotas_bp)

app.run(debug=True)