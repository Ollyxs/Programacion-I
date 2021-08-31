import os
from flask import Flask
from dotenv import load_dotenv


def create_app():
    app = Flask(__name__)
    load_dotenv()

    from main.routes import main, bolsones_ventas, productos
    app.register_blueprint(routes.main.main)
    app.register_blueprint(routes.bolsones_ventas.bolsones_ventas)
    app.register_blueprint(routes.productos.productos)
    return app
