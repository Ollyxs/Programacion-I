from .. import login_manager
from flask import request, flash, redirect, url_for,current_app
from flask_login import UserMixin, LoginManager, current_user
import jwt
from functools import wraps

#Clase que contendrá los datos del usuario logueado
class User(UserMixin):
    def __init__(self ,id ,email ,role):
        self.id = id
        self.email = email
        self.role = role

#Método que le indica a LoginManager como obtener los datos del usuario logueado
#En nuestro caso al trabajar con JWT los datos se obtendran de los claims del Token
#que ha sido guardado en una cookie en el browser
@login_manager.request_loader
def load_user(request):
    #Verificar si la cookie ha sido cargada
    if 'access_token' in request.cookies:
        try:
            #Decodificar el token
            decoded = jwt.decode(request.cookies['access_token'], current_app.config["SECRET_KEY"], algorithms=["HS256"], verify=False)
            #Cargar datos del usuario
            user = User(decoded["id"],decoded["email"],decoded["role"])
            #Devolver usuario logueado con los datos cargados
            return user
        except jwt.exceptions.InvalidTokenError:
            print('Invalid Token.')
        except jwt.exceptions.DecodeError:
            print('DecodeError.')
    return None

#Función que sobreescribe el método al intentar ingresar a una ruta no autorizada
@login_manager.unauthorized_handler
def unauthorized_callback():
    flash('Debe iniciar sesión para continuar.','warning')
    #Redireccionar a la página que contiene el formulario de login
    return redirect(url_for('main.index'))

#Define la función de verificación de admin para las rutas
def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kws):
        if not current_user.role == "admin":
            flash('Acceso restringido a administradores.','warning')
            return redirect(url_for('main.index'))
        return fn(*args, **kws)
    return wrapper

def proveer_required(fn):
    @wraps(fn)
    def wrapper(*args, **kws):
        if not current_user.role == "proveedor":
            flash('Acceso restringido a proveedor.','warning')
            return redirect(url_for('main.index'))
        return fn(*args, **kws)
    return wrapper

def cliente_required(fn):
    @wraps(fn)
    def wrapper(*args, **kws):
        if not current_user.role == "cliente":
            flash('Acceso restringido a cliente.','warning')
            return redirect(url_for('main.index'))
        return fn(*args, **kws)
    return wrapper
