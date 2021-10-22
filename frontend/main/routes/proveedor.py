from flask import Blueprint, render_template, redirect, url_for, current_app, request
from .. formularios.registrarse import FormRegistro
from .. formularios.proveedores import FormFilterProveedor
from flask_login import login_required, LoginManager, current_user
import requests, json
from .auth import admin_required, proveerdor_required


proveedores = Blueprint('proveedores', __name__, url_prefix='/proveedores')


@proveedores.route('/registrar', methods=['POST', 'GET'])
def registrar():
    form = FormRegistro()
    if form.validate_on_submit():
        print(form.nombre.data)
        return redirect(url_for('main.index'))
    return render_template('crear_proveedor.html', formulario=form)

@proveedores.route('/ver/<int:id>')
def ver(id):
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    r = requests.get(
            current_app.config["API_URL"]+'/proveedor/'+str(id),
            headers = headers)
    if (r.status_code == 404):
        return redirect(url_for('proveedores.ver_todos'))
    proveedor = json.loads(r.text)
    return render_template('modificar_proveedor.html', proveedor = proveedor)

@proveedores.route('/todos')
@login_required
@admin_required
def ver_todos():
    filter = FormFilterProveedor(request.args, meta={'csrf': False})
    data = {}
    data['page'] = 1
    data['per_page'] = 1
    if 'page' in request.args:
        data['page'] = request.args.get('page','')
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    if filter.envio():
        if filter.ordenamiento.data != None:
            data["ordenamiento"] =  filter.ordenamiento.data

    r = requests.get(
            current_app.config["API_URL"]+'/proveedores',
            headers = headers,
            data = json.dumps(data))
    proveedores = json.loads(r.text)["proveedores"]
    pagination = {}
    pagination["pages"] = json.loads(r.text)["pages"]
    pagination["current_page"] = json.loads(r.text)["page"]
    return render_template('proveedores_admin.html', proveedores = proveedores, pagination = pagination, filter = filter)
