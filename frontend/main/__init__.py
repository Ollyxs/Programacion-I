import os
from flask import Flask
from dotenv import load_dotenv
from flask_wtf import CSRFProtect


CSRFP = CSRFProtect()


def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config['API_URL'] = os.getenv('API_URL')
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    CSRFP.init_app(app)

    from main.routes import main, bolsones, productos, usuario, proveedor
    app.register_blueprint(routes.main.main)
    app.register_blueprint(routes.bolsones.bolsones)
    app.register_blueprint(routes.productos.productos)
    app.register_blueprint(routes.usuario.usuarios)
    app.register_blueprint(routes.proveedor.proveedores)
    return app
