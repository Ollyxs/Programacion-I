from flask import Blueprint, url_for, render_template, redirect, current_app, request, flash
from .. formularios.producto import FormProducto, FormFilterProducto
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
    return render_template('producto.html', producto = producto)

@productos.route('/todos')
@login_required
@admin_provider_required
def ver_todos():
    filter = FormFilterProducto(request.args, meta={'csrf': False})
    data = {}
    data['page'] = 1
    data['per_page'] = 4
    if 'page' in request.args:
        data["page"] = request.args.get('page','')
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    
    data_prov = {}
    data_prov['page'] = 1
    r = requests.get(
            current_app.config['API_URL']+'/proveedores',
            headers = headers,
            data = json.dumps(data_prov))
    proveedores = [(item['id'], item['nombre']+" "+item['apellido']) for item in json.loads(r.text)["proveedores"]]
    proveedores.insert(0, (0, "Proveedor"))
    filter.proveedorid.choices = proveedores

    if filter.envio():
        if filter.proveedorid.data != None and filter.proveedorid.data != 0:
            data["proveedorid"] = filter.proveedorid.data
        if filter.ordenamiento.data != None:
            data["ordenamiento"] = filter.ordenamiento.data

    r = requests.get(
            current_app.config['API_URL']+'/productos',
            headers=headers,
            data = json.dumps(data))
    productos = json.loads(r.text)["productos"]
    pagination = {}
    pagination["pages"] = json.loads(r.text)["pages"]
    pagination["current_page"] = json.loads(r.text)["page"]
    return render_template('productos_admin.html', productos=productos, pagination=pagination, filter=filter)

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
        r = requests.post(
                current_app.config['API_URL']+'/productos',
                headers = headers,
                data = json.dumps(data))
        if (r.status_code == 201):
            flash('Producto creado.','success')
            return redirect(url_for('productos.ver_todos'))
    return render_template('crear_producto.html', formulario=form)

@productos.route('/eliminar/<int:id>')
@admin_provider_required
def eliminar(id):
    auth = request.cookies['access_token']
    headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer '+auth}
    r = requests.delete(
            current_app.config['API_URL']+'/producto/'+str(id),
            headers = headers)
    if (r.status_code == 204):
        flash('Producto eliminado.', 'success')
    elif (r.status_code == 404):
        flash('Producto no encontrado', 'danger')
    elif (r.status_code == 405):
        flash('No se puede eliminar el producto porque permanece a un bolson en venta.', 'warning')
    return redirect(url_for('productos.ver_todos'))
