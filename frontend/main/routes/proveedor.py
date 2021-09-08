from flask import Blueprint, render_template, redirect, url_for
from .. formularios.registrarse import FormRegistro


proveedores = Blueprint('proveedores', __name__, url_prefix='/proveedores')


@proveedores.route('/registrar', methods=['POST', 'GET'])
def registrar():
    form = FormRegistro()
    if form.validate_on_submit():
        print(form.nombre.data)
        return redirect(url_for('main.index'))
    return render_template('crear_proveedor.html', formulario=form)
