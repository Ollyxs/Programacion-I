from flask import Blueprint, render_template, redirect, url_for, current_app, request, flash
from .. formularios.registrarse import FormRegistro
from .. formularios.ingresar import FormIngreso
from .. formularios.cuenta import FormCuenta
from .. formularios.clientes import FormFilterCliente
from flask_login import login_required, LoginManager, current_user
import requests, json
from .auth import admin_required, admin_client_required, cliente_required, admin_provider_required


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
        headers = {"content-type": "application/json"}
        r = requests.post(
                current_app.config["API_URL"]+'/auth/register',
                headers = headers,
                data = json.dumps(data))
        if (r.status_code == 201):
            flash('Registro exitoso.', 'success')
        elif (r.status_code == 409):
            flash('Email duplicado.', 'warning')
        return redirect(url_for('main.index'))
    return render_template('registrarse.html', formulario=form)

@usuarios.route('/ingresar', methods=['POST', 'GET'])
def ingresar():
    form = FormIngreso()
    if form.validate_on_submit():
        data = {}
        data["email"] = form.email.data
        data["password"] = form.password.data
        headers = {"content-type": "application/json"}
        r = requests.post(
                current_app.config["API_URL"]+'/auth/login',
                headers = headers,
                data = json.dumps(data))
        if (r.status_code == 404):
            flash('Contraseña incorrecta.', 'warning')
            return redirect(url_for('usuarios.ingresar'))
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
            headers = headers)
    r = requests.get(
            current_app.config["API_URL"]+'/proveedor/'+str(id),
            headers = headers)
    if (r.status_code == 404):
        return redirect(url_for('main.index'))
    usuario = json.loads(r.text)
    return render_template('usuario.html', usuario = usuario)

@usuarios.route('cuenta/<int:id>', methods=['POST', 'GET'])
@login_required
@cliente_required
def cliente(id):
    form = FormCuenta()
    auth = request.cookies['access_token']
    headers = {
            "content-type": "application/json",
            'authorization': "Bearer "+auth}
    r = requests.get(
            current_app.config["API_URL"]+'/cliente/'+str(id),
            headers = headers)
    usuario = json.loads(r.text)
    print(usuario)
    if form.validate_on_submit():
        data = {}
        data["nombre"] = form.nombre.data
        data["apellido"] = form.apellido.data
        data["email"] = form.email.data
        data["telefono"] = form.telefono.data
        data["contra"] = form.password.data
        print(form.nombre.data)
        print(form.telefono.data)
        print(data)
        r = requests.put(
                current_app.config["API_URL"]+'/cliente/'+str(id),
                headers = headers,
                data = json.dumps(data))
        if (r.status_code == 201):
            flash('Perfil actualizado.', 'success')
        elif (r.status_code == 401):
            flash('Contraseña incorrecta.', 'danger')
        return redirect(url_for('usuarios.cliente', id=str(id)))
    if (r.status_code == 404):
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('admin.html', usuario=usuario, formulario=form)


@usuarios.route('proveedor/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_provider_required
def proveedor(id):
    form = FormCuenta()
    auth = request.cookies['access_token']
    headers = {
            "content-type": "application/json",
            'authorization': "Bearer "+auth}
    r = requests.get(
            current_app.config["API_URL"]+'/proveedor/'+str(id),
            headers = headers)
    usuario = json.loads(r.text)
    print(usuario)
    if form.validate_on_submit():
        data = {}
        data["nombre"] = form.nombre.data
        data["apellido"] = form.apellido.data
        data["email"] = form.email.data
        data["telefono"] = form.telefono.data
        data["contra"] = form.password.data
        print(form.nombre.data)
        print(form.telefono.data)
        print(data)
        r = requests.put(
                current_app.config["API_URL"]+'/proveedor/'+str(id),
                headers = headers,
                data = json.dumps(data))
        if (r.status_code == 201):
            flash('Perfil actualizado.', 'success')
        elif (r.status_code == 401):
            flash('Contraseña incorrecta.', 'danger')
        return redirect(url_for('usuarios.proveedor', id=str(id)))
    if (r.status_code == 404):
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('admin.html', usuario=usuario, formulario=form)


@usuarios.route('/clientes')
@login_required
@admin_required
def ver_clientes():
    filter = FormFilterCliente(request.args, meta={'csrf': False})
    data = {}
    data['page'] = 1
    data['per_page'] = 10
    if 'page' in request.args:
        data['page'] = request.args.get('page','')
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    if filter.envio():
        if filter.ordenamiento.data != None:
            data["ordenamiento"] = filter.ordenamiento.data
    r = requests.get(
            current_app.config["API_URL"]+'/clientes',
            headers = headers,
            data = json.dumps(data))
    clientes = json.loads(r.text)["clientes"]
    pagination = {}
    pagination["pages"] = json.loads(r.text)["pages"]
    pagination["current_page"] = json.loads(r.text)["page"]
    return render_template('clientes_admin.html', clientes = clientes, pagination = pagination, filter = filter)


# @usuarios.route('admin/<int:id>')
# @login_required
# def mi_cuenta_admin(id):
#     auth = request.cookies['access_token']
#     headers = {
#             "content-type": "application/json",
#             'authorization': "Bearer "+auth}
#     r = requests.get(
#             current_app.config["API_URL"]+'/admin/'+str(id),
#             headers = headers)
#     if (r.status_code == 404):
#         return redirect(url_for('main.index'))
#     usuario = json.loads(r.text)
#     return render_template('admin.html', usuario = usuario)

@usuarios.route('admin/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_required
def admin(id):
    form = FormCuenta()
    auth = request.cookies['access_token']
    headers = {
            "content-type": "application/json",
            'authorization': "Bearer "+auth}
    r = requests.get(
            current_app.config["API_URL"]+'/admin/'+str(id),
            headers = headers)
    usuario = json.loads(r.text)
    print(usuario)
    if form.validate_on_submit():
        data = {}
        data["nombre"] = form.nombre.data
        data["apellido"] = form.apellido.data
        data["email"] = form.email.data
        data["telefono"] = form.telefono.data
        data["contra"] = form.password.data
        print(form.nombre.data)
        print(form.telefono.data)
        print(data)
        r = requests.put(
                current_app.config["API_URL"]+'/admin/'+str(id),
                headers = headers,
                data = json.dumps(data))
        if (r.status_code == 201):
            flash('Perfil actualizado.', 'success')
        elif (r.status_code == 401):
            flash('Contraseña incorrecta.', 'danger')
        return redirect(url_for('usuarios.admin', id=str(id)))
    if (r.status_code == 404):
        flash('Usuario no encontrado.', 'danger')
        return redirect(url_for('main.index'))
    return render_template('admin.html', usuario=usuario, formulario=form)

@usuarios.route('eliminar/<int:id>')
@login_required
@admin_client_required
def eliminar(id):
    auth = request.cookies['access_token']
    headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer '+auth}
    r = requests.delete(
            current_app.config['API_URL']+'/cliente/'+str(id),
            headers = headers)
    if (r.status_code == 404):
        flash('El usuario no existe', 'danger')
        return redirect(url_for('usuarios.ver_clientes'))
    flash('Usuario eliminado', 'success')
    return redirect(url_for('usuarios.ver_clientes'))

@usuarios.route('enviar-promocion')
@login_required
@admin_required
def promocion():
    auth = request.cookies['access_token']
    headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer '+auth}
    r = requests.post(
            current_app.config['API_URL']+'/mail/promo',
            headers = headers)
    if (r.status_code == 409):
        flash(r.text, 'danger')
        return redirect(url_for('usuarios.ver_clientes'))
    flash('Enviado.', 'success')
    return redirect(url_for('usuarios.ver_clientes'))
