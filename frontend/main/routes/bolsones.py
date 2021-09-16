from flask import Blueprint, request, url_for, render_template

bolsones = Blueprint('bolsones', __name__, url_prefix='/bolson')

@bolsones.route('/ver/<int:id>')
def ver(id):
    return render_template('bolson.html')

@bolsones.route('/ver-todos')
def ver_todos():
    return render_template('bolsones.html')
