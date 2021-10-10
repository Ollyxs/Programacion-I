from flask import Blueprint, url_for, render_template, redirect, current_app
from .. formularios.producto import FormProducto
import requests, json


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

@productos.route('/crear_producto', methods=['POST', 'GET'])
def crear_producto():
    form = FormProducto()
    if form.validate_on_submit():
        print(form.nombre.data)
        return redirect(url_for('productos.ver'))
    return render_template('crear_producto.html', formulario=form)
