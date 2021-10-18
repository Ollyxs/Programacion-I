from flask import Blueprint, url_for, render_template, redirect, current_app, request
from .. formularios.producto import FormProducto
from flask_login import login_required, current_user, LoginManager
import requests, json
from .auth import admin_required, proveerdor_required, admin_provider_required


productos = Blueprint('productos', __name__, url_prefix='/productos')


@productos.route('/ver/<int:id>')
def ver(id):
    r = requests.get(
            current_app.config['API_URL']+'/producto/'+str(id),
            headers = {"content-type": "application/json"})
    if (r.status_code == 404):
        return redirect(url_for('main.index'))
    producto = json.loads(r.text)
    print(producto)
    return render_template('producto.html', producto = producto)

@productos.route('/todos')
@login_required
@admin_provider_required
def ver_todos():
    data = {}
    data['page'] = 1
    data['per_page'] = 10
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    print(data)
    r = requests.get(
            current_app.config['API_URL']+'/productos',
            headers=headers,
            data = json.dumps(data))
    productos = json.loads(r.text)["productos"]
    return render_template('productos_admin.html', productos=productos)

@productos.route('/crear', methods=['POST', 'GET'])
@proveerdor_required
def crear():
    form = FormProducto()

    if form.validate_on_submit():
        auth = request.cookies['access_token']
        headers = {'content-type': 'application/json',
                'authorization': 'Bearer '+auth}
        data = {}
        data["nombre"] = form.nombre.data
        data["descripcion"] = form.descripcion.data
        print(data)
        r = requests.post(
                current_app.config['API_URL']+'/productos',
                headers = headers,
                data = json.dumps(data))
        if (r.status_code == 201):
            return redirect(url_for('productos.ver_todos'))
    return render_template('crear_producto.html', formulario=form)
