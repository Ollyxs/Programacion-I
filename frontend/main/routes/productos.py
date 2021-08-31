from flask import Blueprint, url_for, render_template

productos = Blueprint('productos', __name__, url_prefix='/productos')


@productos.route('/ver/<int:id>')
def ver(id):
    return render_template('producto.html')
