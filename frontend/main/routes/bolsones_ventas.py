from flask import Blueprint, request, url_for, render_template

bolsones_ventas = Blueprint('bolsones_ventas', __name__, url_prefix='/bolson')

@bolsones_ventas.route('/ver/<int:id>')
def ver(id):
    return render_template('bolson_en_venta.html')

@bolsones_ventas.route('/ver-todos')
def ver_todos():
    return render_template('bolsones.html')
