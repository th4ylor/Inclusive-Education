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

<<<<<<< HEAD
createTable()
=======
createTable()
>>>>>>> ddc0a1d2551b09c13369f983a6c36d79bad97ad1
