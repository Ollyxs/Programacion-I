from flask import Blueprint, render_template, redirect, url_for, current_app, request, flash
from flask_login import login_required, LoginManager, current_user
from .. formularios.compra import FormFilterCompra
import requests, json
from .auth import admin_required, cliente_required


compras = Blueprint('compras', __name__, url_prefix='/compras')


@compras.route('/ver/<int:id>')
@login_required
@admin_required
def ver(id):
    user = current_user
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    r = requests.get(
            current_app.config['API_URL']+'/compra/'+str(id),
            headers = headers)
    if (r.status_code == 404):
        return redirect(url_for('compras.ver_todas'))
    compra = json.loads(r.text)
    print(compra)
    return render_template('ver_modificar_compra.html', compra = compra, user = user)

@compras.route('/todas')
@login_required
@admin_required
def ver_todas():
    filter = FormFilterCompra(request.args, meta={'csrf': False})
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
        if filter.nombre.data != None:
            data['nombre'] = filter.nombre.data
        if filter.apellido.data != None:
            data['apellido'] = filter.apellido.data
        if filter.retirado != None:
            data['retirado'] = filter.retirado.data
        if filter.ordenamiento.data != None:
            data['ordenamiento'] = filter.ordenamiento.data

    r = requests.get(
            current_app.config['API_URL']+'/compras',
            headers = headers,
            data = json.dumps(data))
    compras = json.loads(r.text)["compras"]
    pagination = {}
    pagination["pages"] = json.loads(r.text)["pages"]
    pagination["current_page"] = json.loads(r.text)["page"]
    return render_template('compras_admin.html', compras = compras, pagination = pagination, filter = filter)

@compras.route('comprar/<int:id>')
@login_required
@cliente_required
def comprar(id):
    auth = request.cookies['access_token']
    headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer '+auth}
    data = {}
    data["bolsonid"] = id
    r = requests.post(
            current_app.config['API_URL']+'/compras',
            headers = headers,
            data = json.dumps(data))
    if (r.status_code == 201):
        flash('Compra exitosa.', 'success')
        return redirect(url_for('main.index'))
    return render_template('main.index')

@compras.route('mis-compras')
@login_required
@cliente_required
def mis_compras():
    data = {}
    data['page'] = 1
    data['per_page'] = 10
    if 'page' in request.args:
        data['page'] = request.args.get('page','')
    auth = request.cookies['access_token']
    headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer '+auth}

    r = requests.get(
            current_app.config['API_URL']+'/compras',
            headers = headers,
            data=json.dumps(data))
    compras = json.loads(r.text)["compras"]
    pagination = {}
    pagination['pages'] = json.loads(r.text)['pages']
    pagination['current_page'] = json.loads(r.text)['page']
    return render_template('mis_compras.html', compras = compras, pagination = pagination)

@compras.route('retirado/<int:id>')
@login_required
@admin_required
def retirado(id):
    auth = request.cookies['access_token']
    headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer '+auth}
    data = {}
    data['retirado'] = 1
    r = requests.put(
            current_app.config['API_URL']+'/compra/'+str(id),
            headers = headers,
            data = json.dumps(data))
    if (r.status_code == 201):
        flash('Compra retirada.', 'success')
    return redirect(url_for('compras.ver_todas'))

@compras.route('no-retirado/<int:id>')
@login_required
@admin_required
def no_retirado(id):
    auth = request.cookies['access_token']
    headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer '+auth}
    data = {}
    data['retirado'] = 0
    r = requests.put(
            current_app.config['API_URL']+'/compra/'+str(id),
            headers = headers,
            data = json.dumps(data))
    if (r.status_code == 201):
        flash('Compra no retirada.', 'warning')
    return redirect(url_for('compras.ver_todas'))

@compras.route('/eliminar/<int:id>')
@login_required
@admin_required
def eliminar(id):
    auth = request.cookies['access_token']
    headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer '+auth}
    r = requests.delete(
            current_app.config['API_URL']+'/compra/'+str(id),
            headers = headers)
    if r.status_code == 404:
        flash('Compra no encontrada.', 'danger')
    else:
        flash('Compra eliminada.', 'success')
    return redirect(url_for('compras.ver_todas'))
