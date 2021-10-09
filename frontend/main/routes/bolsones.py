from flask import Blueprint, redirect, url_for, render_template, current_app
from .productos import PRODUCTOS
import requests, json

bolsones = Blueprint('bolsones', __name__, url_prefix='/bolson')

BOLSONES = [
        {"id":0,"nombre":"Carnes","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","producto":0},
        {"id":1,"nombre":"Panadería","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","producto":2},
        {"id":2,"nombre":"Verdulería","precio":"$99.99","aprobado":False,"fecha":"2021-09-13","producto":4},
        {"id":3,"nombre":"Lacteos","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","producto":5},
        {"id":4,"nombre":"Limpieza","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","producto":6},
        {"id":5,"nombre":"Fiambrería","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","producto":7},
        {"id":6,"nombre":"Bebidas","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","producto":8},
        {"id":7,"nombre":"Legumbres","precio":"99.99","aprobado":True,"fecha":"2021-09-13","producto":9}
        ]


@bolsones.route('/ver/<int:id>')
def ver(id):
    r = requests.get(
            current_app.config["API_URL"]+'/bolson/'+str(id),
            headers={"content-type": "application/json"})
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
    print(current_app.config["API_URL"]+'/bolsones')
    r = requests.get(
        current_app.config["API_URL"]+'/bolsones',
        headers={"content-type":"application/json"},
        data=json.dumps(data))
    bolsones = json.loads(r.text)["bolsones"] 
    return render_template('bolsones.html', bolsones = bolsones)
