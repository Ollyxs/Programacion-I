from flask import Blueprint, render_template, redirect, url_for, current_app, request
from flask_login import login_required, LoginManager, current_user
from .. formularios.compra import FormCompra, FormFilterCompra
import requests, json
from .auth import admin_required, cliente_required


compras = Blueprint('compras', __name__, url_prefix='/compras')


@compras.route('/ver/<int:id>')
@login_required
@admin_required
def ver(id):
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
    return render_template('ver_modificar_compra.html', compra = compra)

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

    print(data)

    r = requests.get(
            current_app.config['API_URL']+'/compras',
            headers = headers,
            data = json.dumps(data))
    print(r)
    compras = json.loads(r.text)["compras"]
    return render_template('compras_admin.html', compras = compras, filter = filter)

@compras.route('/crear', methods=['POST', 'GET'])
@login_required
def crear():
    form = FormCompra()
    if form.validate_on_submit():
        data = {}
        data["bolsonid"] = form.bolsonid.data
        print(data)
        auth = request.cookies['access_token']
        headers = {
                'content-type': 'application/json',
                'authorization': 'Bearer '+auth}
        r = requests.post(
                current_app.config['API_URL']+'/compras',
                headers = headers,
                data = json.dumps(data))
        if (r.status_code == 201):
            return redirect(url_for('main.index'))
    return render_template('bolson.html', form = form)
