from flask import Blueprint, url_for, render_template
from . import bolsones

main = Blueprint('main', __name__, url_prefix='/')

BOLSONES = [
        {"id":0,"nombre":"Carnes","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","productos":"milanesa"},
        {"id":1,"nombre":"Panadería","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","productos":"pan"},
        {"id":2,"nombre":"Verdulería","precio":"$99.99","aprobado":False,"fecha":"2021-09-13","productos":"papa"},
        {"id":3,"nombre":"Lacteos","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","productos":"leche"},
        {"id":4,"nombre":"Limpieza","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","productos":"jabón"},
        {"id":5,"nombre":"Fiambrería","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","productos":"jamon"},
        {"id":6,"nombre":"Bebidas","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","productos":"vino"},
        {"id":7,"nombre":"Legumbres","precio":"$99.99","aprobado":True,"fecha":"2021-09-13","productos":"fideos"}
        ]

@main.route('/')
def index():
    return render_template('index.html', bolsones = BOLSONES)
