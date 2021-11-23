from flask import Blueprint, url_for, render_template, current_app, redirect, request, make_response, flash
from .. formularios.ingresar import FormIngreso
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from . import usuario
import requests, json
from .auth import User


main = Blueprint('main', __name__, url_prefix='/')


@main.route('/')
def index():
    data = {}
    data['page'] = 1
    r = requests.get(
            current_app.config['API_URL']+'/bolsones-venta',
            headers ={"content-type": "application/json"},
            data = json.dumps(data))
    bolsones = json.loads(r.text)["bolsonesventas"]
    return render_template('index.html', bolsones = bolsones)

@main.route('/ingresar', methods=['POST'])
def login():
    form = FormIngreso()
    if form.validate_on_submit():
        data = '{"email":"'+form.email.data+'", "password":"'+form.password.data+'"}'
        r = requests.post(
                current_app.config["API_URL"]+'/auth/login',
                headers={"content-type": "application/json"},
                data = data)
        if r.status_code == 200:
            user_data = json.loads(r.text)
            user = User(id = user_data.get("id"), email = user_data.get("email"), role = user_data.get("role"))
            login_user(user)
            req = make_response(redirect(url_for('main.index')))
            req.set_cookie('access_token', user_data.get("access_token"), httponly = True)
            return req
        else:
            flash('Usuario o contraseña incorrecta', 'danger')
            return redirect(url_for('usuarios.ingresar'))
    return redirect(url_for('main.index'))

@main.route('/cerrar-sesion')
def logout():
    req = make_response(redirect(url_for('main.index')))
    req.set_cookie('access_token', '', httponly = True)
    logout_user()
    return req

@main.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@main.route('/zona-de-retiro')
def retiro():
    return render_template('zona_retiro.html')

@main.route('/ayuda')
def ayuda():
    return render_template('preguntas.html')
