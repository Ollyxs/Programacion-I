from flask import Blueprint, url_for, render_template, redirect
from .. formularios.producto import FormProducto
from .usuario import USUARIOS

productos = Blueprint('productos', __name__, url_prefix='/productos')

PRODUCTOS = [
        {"id":0,"nombre":"Milanesa","descripcion":"1kg de milanesa de carne.","proveedorid":2},
        {"id":1,"nombre":"Pollo","descripcion":"Pollo casero.","proveedorid":2},
        {"id":2,"nombre":"Pan","descripcion":"1kg de pan bollito.","proveedorid":1},
        {"id":3,"nombre":"Facturas","descripcion":"1 docena de facturas de manteca.","proveedorid":1},
        {"id":4,"nombre":"Papa","descripcion":"3kg de papa","proveedorid.":2},
        {"id":5,"nombre":"Leche","descripcion":"1 caja de leche entera.","proveedorid":3},
        {"id":6,"nombre":"Jabón","descripcion":"Jabón de tocador x3 unidades.","proveedorid":4},
        {"id":7,"nombre":"Jamón","descripcion":"500g de jamón cocido.","proveedorid":5},
        {"id":8,"nombre":"Vino","descripcion":"1 damajuana de vino tinto.","proveedorid":6},
        {"id":9,"nombre":"Fideos","descripcion":"1 paquete de fideos tallarin.","proveedorid":7}
        ]


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
