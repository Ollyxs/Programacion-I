from flask import Blueprint, redirect, url_for, render_template, current_app, request
from .. formularios.bolson import FormBolson, FormFilterBolson, FormFilterBolsones
from flask_login import login_required, LoginManager, current_user
import requests, json
from .auth import admin_required, proveerdor_required, cliente_required, admin_provider_required, admin_client_required


bolsones = Blueprint('bolsones', __name__, url_prefix='/bolson')


@bolsones.route('/<int:id>')
@login_required
@admin_required
def ver(id):
    user = current_user
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    r = requests.get(
            current_app.config["API_URL"]+'/bolson/'+str(id),
            headers = headers)
    if (r.status_code == 404):
        return redirect(url_for('bolsones.ver_todos'))
    bolson = json.loads(r.text)
    return render_template('bolson.html', bolson = bolson, user = user)

@bolsones.route('/todos')
@login_required
@admin_required
def ver_todos():
    user = current_user
    filter = FormFilterBolsones(request.args, meta={'csrf': False})
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    
    data = {}
    data['page'] = 1
    data['per_page'] = 10
    if 'page' in request.args:
        data['page'] = request.args.get('page','')
    
    if filter.envio():
        if filter.desde.data != None:
            data['desde'] = filter.desde.data.strftime('%Y-%m-%d')
        if filter.hasta.data != None:
            data['hasta'] = filter.hasta.data.strftime('%Y-%m-%d')

    print(data)

    r = requests.get(
        current_app.config["API_URL"]+'/bolsones',
        headers = headers,
        data = json.dumps(data))
    bolsones = json.loads(r.text)["bolsones"] 
    pagination = {}
    pagination["pages"] = json.loads(r.text)["pages"]
    pagination["current_page"] = json.loads(r.text)["page"] 
    return render_template('bolsones_admin.html', bolsones = bolsones, pagination = pagination, filter = filter, user = user)

@bolsones.route('/ver/<int:id>')
def ver_en_venta(id):
    user = current_user
    r = requests.get(
            current_app.config["API_URL"]+'/bolson-venta/'+str(id),
            headers = {"content-type": "application/json"})
    if (r.status_code == 404):
        return redirect(url_for('bolsones.ver_todos_en_venta'))
    bolson = json.loads(r.text)
    return render_template('bolson.html', bolson = bolson, user = user)

@bolsones.route('/ver-todos')
def ver_todos_en_venta():
    filter = FormFilterBolson(request.args, meta={'csrf': False})
    data = {}
    data['page'] = 1
    data['per_page'] = 12
    if 'page' in request.args:
        data['page'] = request.args.get('page','')
    headers = {'content-type':'application/json'}
    
    if filter.envio():
        if filter.nombre.data != None:
            data["nombre"] = filter.nombre.data
        if filter.desde.data != None:
            data["desde"] = filter.desde.data
        if filter.hasta.data != None:
            data["hasta"] = filter.hasta.data
        if filter.ordenamiento.data != None:
            data["ordenamiento"] = filter.ordenamiento.data

    r = requests.get(
        current_app.config["API_URL"]+'/bolsones-venta',
        headers = headers,
        data = json.dumps(data))
    bolsones = json.loads(r.text)["bolsonesventas"]
    pagination = {}
    pagination["pages"] = json.loads(r.text)["pages"]
    pagination["current_page"] = json.loads(r.text)["page"]
    return render_template('bolsones.html', bolsones = bolsones, pagination = pagination, filter = filter)

@bolsones.route('/pendiente/<int:id>', methods=['POST', 'GET'])
@login_required
@admin_provider_required
def ver_pendiente(id):
    user = current_user
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    r = requests.get(
            current_app.config["API_URL"]+'/bolson-pendiente/'+str(id),
            headers = headers)
    if (r.status_code == 404):
        return redirect(url_for('main.index'))
    bolson = json.loads(r.text)
    return render_template('bolson.html', bolson = bolson, user = user)

@bolsones.route('/pendientes')
@login_required
@admin_provider_required
def ver_pendientes():
    user = current_user
    filter = FormFilterBolsones(request.args, meta={'csrf': False})
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}

    data = {}
    data['page'] = 1
    data['per_page'] = 10
    if 'page' in request.args:
        data['page'] = request.args.get('page','')

    if filter.envio():
        if filter.desde.data != None:
            data['desde'] = filter.desde.data.strftime('%Y-%m-%d')
        if filter.hasta.data != None:
            data['hasta'] = filter.hasta.data.strftime('%Y-%m-%d')

    r = requests.get(
            current_app.config["API_URL"]+'/bolsones-pendientes',
            headers = headers,
            data = json.dumps(data))
    bolsones = json.loads(r.text)["bolsones pendientes"]
    pagination = {}
    pagination["pages"] = json.loads(r.text)["pages"]
    pagination["current_page"] = json.loads(r.text)["page"]
    return render_template('bolsones_pendientes.html', bolsones = bolsones, pagination = pagination, filter = filter, user = user)

@bolsones.route('/previo/<int:id>')
@login_required
@admin_required
def ver_previo(id):
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    r = requests.get(
            current_app.config["API_URL"]+'/bolson-previo/'+str(id),
            headers = headers)
    if (r.status_code == 404):
        return redirect(url_for('bolsones.ver_todos'))
    bolson = json.loads(r.text)
    return render_template('bolson.html', bolson = bolson)

@bolsones.route('/previos')
@login_required
@admin_required
def ver_previos():
    user = current_user
    filter = FormFilterBolsones(request.args, meta={'csrf': False})
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    data = {}
    data['page'] = 1
    data['per_page'] = 10
    if 'page' in request.args:
        data['page'] = request.args.get('page','')

    if filter.envio():
        if filter.desde.data != None:
            data['desde'] = filter.desde.data.strftime('%Y-%m-%d')
        if filter.hasta.data != None:
            data['hasta'] = filter.hasta.data.strftime('%Y-%m-%d')

    r = requests.get(
        current_app.config["API_URL"]+'/bolsones-previos',
        headers = headers,
        data = json.dumps(data))
    bolsones = json.loads(r.text)["bolsones previos"] 
    pagination = {}
    pagination["pages"] = json.loads(r.text)["pages"]
    pagination["current_page"] = json.loads(r.text)["page"]
    return render_template('bolsones_previos.html', bolsones = bolsones, pagination = pagination, filter = filter, user = user)

@bolsones.route('/crear', methods=['POST', 'GET'])
@login_required
@admin_required
def crear():
    form = FormBolson()
    data = {}
    data['page'] = 1
    auth = request.cookies['access_token']
    headers = {
            'content-type': "application/json",
            'authorization': "Bearer "+auth}
    r = requests.get(
            current_app.config["API_URL"]+'/productos',
            headers = headers,
            data = json.dumps(data))
    productos = [(item['id'], item['nombre']+"\n - "+item['proveedor']) for item in json.loads(r.text)["productos"]]

    form.productosId.choices = productos
    if form.validate_on_submit():
        auth = request.cookies['access_token']
        headers = {
                'content-type': 'application/json',
                'authorization': 'Bearer '+auth}
        data = {}
        data["nombre"] = form.nombre.data
        data["fecha"] = form.fecha.data.strftime("%Y-%m-%d")
        data["precio"] = form.precio.data
        data["productos"] = form.productosId.data
        print(data)
        r = requests.post(
                current_app.config["API_URL"]+'/bolsones-pendientes',
                headers = headers,
                data = json.dumps(data))
        if (r.status_code == 201):
            return redirect(url_for('bolsones.ver_pendientes'))
        print(r)
    return render_template('crear_bolson.html', form = form)

@bolsones.route('eliminar/<int:id>')
@login_required
@admin_required
def eliminar(id):
    auth = request.cookies['access_token']
    headers = {
            'content-Type': "application/json",
            'authorization': "Bearer "+auth}
    r = requests.delete(
            current_app.config["API_URL"]+'/bolson-pendiente/'+str(id),
            headers = headers)
    if (r.status_code == 404):
        return redirect(url_for('bolsones.ver_todos'))
    return redirect(url_for('bolsones.ver_todos'))

@bolsones.route('aprobar/<int:id>')
@login_required
@admin_required
def aprobar(id):
    auth = request.cookies['access_token']
    headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer '+auth}
    data = {}
    data["aprobado"] = 1
    r = requests.put(
            current_app.config['API_URL']+'/bolson-pendiente/'+str(id),
            headers=headers,
            data = json.dumps(data))
    if (r.status_code == 201):
        return redirect(url_for('bolsones.ver_todos'))
    return redirect(url_for('bolsones.ver_todos'))

@bolsones.route('desaprobar/<int:id>')
@login_required
@admin_required
def desaprobar(id):
    auth = request.cookies['access_token']
    headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer '+auth}
    data = {}
    data["aprobado"] = 0
    r = requests.put(
            current_app.config['API_URL']+'/bolson-pendiente/'+str(id),
            headers=headers,
            data = json.dumps(data))
    if (r.status_code == 201):
        return redirect(url_for('bolsones.ver_todos'))
    return redirect(url_for('bolsones.ver_todos'))
