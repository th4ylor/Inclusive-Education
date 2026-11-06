from flask import Flask
from rotas import rotas_bp
from db import createTable
from metodologias import metodologias_bp
from datetime import timedelta


app = Flask(__name__)

app.register_blueprint(rotas_bp)
app.register_blueprint(metodologias_bp)

app.config.update(
    SECRET_KEY = "chaveExpostadePropositoPorEnquanto",
    SESSION_COOKIE_HTTPONLY =True,
    PERMANENT_SESSION_LIFETIME = timedelta(hours = 2)
)

createTable()
