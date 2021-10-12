from flask import Blueprint, render_template, redirect, url_for, current_app, request
from .. formularios.registrarse import FormRegistro
from .. formularios.ingresar import FormIngreso
from .. formularios.cuenta import FormCuenta
from flask_login import login_required, LoginManager, current_user
import requests, json
from .auth import admin_required


usuarios = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuarios.route('/registrar', methods=['POST', 'GET'])
def registrar():
    form = FormRegistro()
    if form.validate_on_submit():
        data = {}
        data["nombre"] = form.nombre.data
        data["apellido"] = form.apellido.data
        data["email"] = form.email.data
        data["telefono"] = form.telefono.data
        data["password"] = form.password.data
        print(data)
        headers = {"content-type": "application/json"}
        r = requests.post(
                current_app.config["API_URL"]+'/auth/register',
                headers = headers,
                data = json.dumps(data))
        return redirect(url_for('main.index'))
    return render_template('registrarse.html', formulario=form)

@usuarios.route('/ingresar', methods=['POST', 'GET'])
def ingresar():
    form = FormIngreso()
    if form.validate_on_submit():
        data = {}
        data["email"] = form.email.data
        data["password"] = form.password.data
        print(data)
        headers = {"content-type": "application/json"}
        r = requests.post(
                current_app.config["API_URL"]+'/auth/login',
                headers = headers,
                data = json.dumps(data))
        return redirect(url_for('main.index'))
    return render_template('ingresar.html', formulario=form)

@usuarios.route('mi-cuenta/<int:id>')
@login_required
def mi_cuenta(id):
    auth = request.cookies['access_token']
    headers = {
            "content-type": "application/json",
            'authorization': "Bearer "+auth}
    r = requests.get(
            current_app.config["API_URL"]+'/cliente/'+str(id),
            headers = {"content-type": "application/json"})
    if (r.status_code == 404):
        return redirect(url_for('main.index'))
    usuario = json.loads(r.text)
    print(usuario)
    return render_template('usuario.html', usuario = usuario)

@usuarios.route('admin', methods=['POST', 'GET'])
@login_required
@admin_required
def admin():
    form = FormCuenta()
    if form.validate_on_submit():
        print(form.name.data)
        return redirect(url_for('usuario.admin'))
    return render_template('admin.html', formulario=form)
