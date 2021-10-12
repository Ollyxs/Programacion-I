from flask import Blueprint, redirect, url_for, render_template, current_app, request
from .. formularios.bolson import FormBolson
import requests, json


bolsones = Blueprint('bolsones', __name__, url_prefix='/bolson')


@bolsones.route('/<int:id>')
def ver(id):
    r = requests.get(
            current_app.config["API_URL"]+'/bolson/'+str(id),
            headers = {"content-type": "application/json"})
    if (r.status_code == 404):
        return redirect(url_for('bolsones.ver_todos'))
    bolson = json.loads(r.text)
    return render_template('bolson.html', bolson = bolson)

@bolsones.route('/todos')
def ver_todos():
    data = {}
    data['page'] = 1
    data['per_page'] = 10
    print(data)
    r = requests.get(
        current_app.config["API_URL"]+'/bolsones',
        headers = {"content-type":"application/json"},
        data = json.dumps(data))
    bolsones = json.loads(r.text)["bolsones"] 
    r = requests.get(
            current_app.config["API_URL"]+'/bolsones-pendientes',
            headers = {"content-type": "application/json"},
            data = json.dumps(data))
    pendientes = json.loads(r.text)["bolsones pendientes"]
    r = requests.get(
        current_app.config["API_URL"]+'/bolsones-previos',
        headers = {"content-type":"application/json"},
        data = json.dumps(data))
    previos = json.loads(r.text)["bolsones previos"] 
    return render_template('bolsones_admin.html', bolsones = bolsones, pendientes = pendientes, previos = previos)

@bolsones.route('/ver/<int:id>')
def ver_en_venta(id):
    r = requests.get(
            current_app.config["API_URL"]+'/bolson-venta/'+str(id),
            headers = {"content-type": "application/json"})
    if (r.status_code == 404):
        return redirect(url_for('bolsones.ver_todos_en_venta'))
    bolson = json.loads(r.text)
    return render_template('bolson.html', bolson = bolson)

@bolsones.route('/ver-todos')
def ver_todos_en_venta():
    data = {}
    data['page'] = 1
    data['per_page'] = 10
    print(data)
    r = requests.get(
        current_app.config["API_URL"]+'/bolsones-venta',
        headers = {"content-type":"application/json"},
        data = json.dumps(data))
    bolsones = json.loads(r.text)["bolsonesventas"] 
    return render_template('bolsones.html', bolsones = bolsones)

@bolsones.route('/pendiente/<int:id>')
def ver_pendiente(id):
    r = requests.get(
            current_app.config["API_URL"]+'/bolson-pendiente/'+str(id),
            headers = {"content-type": "application/json"})
    if (r.status_code == 404):
        return redirect(url_for('bolsones.ver_pendientes'))
    bolson = json.loads(r.text)
    return render_template('bolson.html', bolson = bolson)

@bolsones.route('/pendientes')
def ver_pendientes():
    data = {}
    data['page'] = 1
    data['per_page'] = 10
    print(data)
    r = requests.get(
            current_app.config["API_URL"]+'/bolsones-pendientes',
            headers = {"content-type": "application/json"},
            data = json.dumps(data))
    bolsones = json.loads(r.text)["bolsones pendientes"]
    return render_template('bolsones_admin.html', bolsones = bolsones)

@bolsones.route('/previo/<int:id>')
def ver_previo(id):
    r = requests.get(
            current_app.config["API_URL"]+'/bolson-previo/'+str(id),
            headers = {"content-type": "application/json"})
    if (r.status_code == 404):
        return redirect(url_for('bolsones.ver_todos'))
    bolson = json.loads(r.text)
    return render_template('bolson.html', bolson = bolson)

@bolsones.route('/previos')
def ver_previos():
    data = {}
    data['page'] = 1
    data['per_page'] = 10
    print(data)
    r = requests.get(
        current_app.config["API_URL"]+'/bolsones-previos',
        headers = {"content-type":"application/json"},
        data = json.dumps(data))
    bolsones = json.loads(r.text)["bolsones"] 
    return render_template('bolsones_admin.html', bolsones = bolsones)

@bolsones.route('/crear', methods=['POST', 'GET'])
def crear():
    form = FormBolson()
    data = {}
    data['page'] = 1
    r = requests.get(
            current_app.config["API_URL"]+'/productos',
            headers = {"content-type": "application/json"},
            data = json.dumps(data))
    productos = [(item['id'], item['nombre']+"\n - "+item['proveedor']) for item in json.loads(r.text)["productos"]]
    print(productos)

    #productos.insert(0, (0, ""))
    form.productosId.choices = productos
    if form.validate_on_submit():
        headers = {'content-type': 'application/json'}
        data = {}
        data["nombre"] = form.nombre.data
        data["fecha"] = form.fecha.data.strftime("%Y-%m-%d")
        # productosId = []
        # if form.productosId.data != 0:
        #     productosId.append(form.productosId.data)
        data["productos"] = form.productosId.data
        print(data)
        r = requests.post(
                current_app.config["API_URL"]+'/bolsones-pendientes',
                headers = headers,
                data = json.dumps(data))
        if (r.status_code == 201):
            return redirect(url_for('bolsones.ver_todos'))
        print(r)
    return render_template('crear_bolson.html', form = form)
        
