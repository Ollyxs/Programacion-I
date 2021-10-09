from flask import Blueprint, url_for, render_template, redirect
from .. formularios.producto import FormProducto


productos = Blueprint('productos', __name__, url_prefix='/productos')


@productos.route('/ver/<int:id>')
def ver(id):
    return render_template('producto.html', producto = PRODUCTOS[id], usuarios = USUARIOS)

@productos.route('/crear_producto', methods=['POST', 'GET'])
def crear_producto():
    form = FormProducto()
    if form.validate_on_submit():
        print(form.nombre.data)
        return redirect(url_for('productos.ver'))
    return render_template('crear_producto.html', formulario=form)
