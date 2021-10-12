from flask import Blueprint, redirect, url_for, render_template, current_app
import requests, json

bolsones = Blueprint('bolsones', __name__, url_prefix='/bolson')

@bolsones.route('/ver/<int:id>')
def ver(id):
    r = requests.get(
            current_app.config["API_URL"]+'/bolson-venta/'+str(id),
            headers = {"content-type": "application/json"})
    if (r.status_code == 404):
        return redirect(url_for('bolsones.ver_todos'))
    bolson = json.loads(r.text)
    return render_template('bolson.html', bolson = bolson)

@bolsones.route('/ver-todos')
def ver_todos():
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

@bolsones.route('/<int:id>')
def ver_bolson(id):
    r = requests.get(
            current_app.config["API_URL"]+'/bolson/'+str(id),
            headers = {"content-type": "application/json"})
    if (r.status_code == 404):
        return redirect(url_for('bolsones.listar_todos'))
    bolson = json.loads(r.text)
    return render_template('bolson.html', bolson = bolson)

@bolsones.route('/todos')
def listar_todos():
    data = {}
    data['page'] = 1
    data['per_page'] = 10
    print(data)
    r = requests.get(
        current_app.config["API_URL"]+'/bolsones',
        headers = {"content-type":"application/json"},
        data = json.dumps(data))
    bolsones = json.loads(r.text)["bolsones"] 
    return render_template('bolsones_admin.html', bolsones = bolsones)

@bolsones.route('/ver-bolson-pendiente/<int:id>')
def ver_pendiente(id):
    r = requests.get(
            current_app.config["API_URL"]+'/bolson-pendiente/'+str(id),
            headers = {"content-type": "application/json"})
    if (r.status_code == 404):
        return redirect(url_for('bolsones.ver_pendientes'))
    bolson = json.loads(r.text)
    return render_template('bolson.html', bolson = bolson)

@bolsones.route('/bolsones-pendientes')
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
