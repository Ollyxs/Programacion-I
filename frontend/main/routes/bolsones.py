from flask import Blueprint, request, url_for, render_template


bolsones = Blueprint('bolsones', __name__, url_prefix='/bolson')

BOLSONES = [
        {"id":0,"nombre":"Carnes","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","productos":"milanesa"},
        {"id":1,"nombre":"Panadería","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","productos":"pan"},
        {"id":2,"nombre":"Verdulería","precio":"$99.99","aprobado":False,"fecha":"2021-09-13","productos":"papa"},
        {"id":3,"nombre":"Lacteos","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","productos":"leche"},
        {"id":4,"nombre":"Limpieza","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","productos":"jabón"},
        {"id":5,"nombre":"Fiambrería","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","productos":"jamon"},
        {"id":6,"nombre":"Bebidas","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","productos":"vino"},
        {"id":7,"nombre":"Legumbres","precio":"99.99","aprobado":True,"fecha":"2021-09-13","productos":"fideos"}
        ]


@bolsones.route('/ver/<int:id>')
def ver(id):
    return render_template('bolson.html', bolson = BOLSONES[id])

@bolsones.route('/ver-todos')
def ver_todos():
    return render_template('bolsones.html', bolsones = BOLSONES)
