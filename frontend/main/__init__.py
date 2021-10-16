import os
from flask import Flask
from dotenv import load_dotenv
from flask_wtf import CSRFProtect
from flask_login import LoginManager


CSRFP = CSRFProtect()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    load_dotenv()

    app.config['API_URL'] = os.getenv('API_URL')
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    CSRFP.init_app(app)
    login_manager.init_app(app)

    from main.routes import main, bolsones, productos, usuario, proveedor, compras
    app.register_blueprint(routes.main.main)
    app.register_blueprint(routes.bolsones.bolsones)
    app.register_blueprint(routes.productos.productos)
    app.register_blueprint(routes.usuario.usuarios)
    app.register_blueprint(routes.proveedor.proveedores)
    app.register_blueprint(routes.compras.compras)
    return app
