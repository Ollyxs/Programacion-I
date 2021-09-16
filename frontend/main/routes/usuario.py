from flask import Blueprint, render_template, redirect, url_for
from .. formularios.registrarse import FormRegistro
from .. formularios.ingresar import FormIngreso


usuarios = Blueprint('usuarios', __name__, url_prefix='/usuarios')


@usuarios.route('/registrar', methods=['POST', 'GET'])
def registrar():
    form = FormRegistro()
    if form.validate_on_submit():
        print(form.nombre.data)
        return redirect(url_for('main.index'))
    return render_template('registrarse.html', formulario=form)

@usuarios.route('/ingresar', methods=['POST', 'GET'])
def ingresar():
    form = FormIngreso()
    if form.validate_on_submit():
        print(form.email.data)
        return redirect(url_for('main.index'))
    return render_template('ingresar.html', formulario=form)
